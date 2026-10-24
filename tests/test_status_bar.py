"""Test the optional status-bar hook without requiring a running NVDA."""

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock, patch


class _DefaultAppModule:
	@property
	def statusBar(self):
		raise NotImplementedError


class _COMError(Exception):
	pass


class TestStatusBarFallback(unittest.TestCase):
	def setUp(self):
		self.original = Mock(return_value=None)
		self.foreground = SimpleNamespace(windowHandle=123, appModule=_DefaultAppModule())
		self.api = ModuleType("api")
		self.api.getStatusBar = self.original
		self.api.getForegroundObject = Mock(return_value=self.foreground)
		self.statusBar = SimpleNamespace(role=27, name="Full status bar text")
		self.accessible = ModuleType("NVDAObjects.IAccessible")
		self.accessible.getNVDAObjectFromEvent = Mock(return_value=self.statusBar)
		nvdaObjects = ModuleType("NVDAObjects")
		nvdaObjects.IAccessible = self.accessible
		self.windowUtils = ModuleType("windowUtils")
		self.windowUtils.findDescendantWindow = Mock(return_value=456)
		controlTypes = ModuleType("controlTypes")
		controlTypes.Role = SimpleNamespace(STATUSBAR=27)
		winUser = ModuleType("winUser")
		winUser.OBJID_CLIENT = -4
		comtypes = ModuleType("comtypes")
		comtypes.COMError = _COMError
		self.logger = Mock()
		logHandler = ModuleType("logHandler")
		logHandler.log = self.logger
		dependencies = {
			"api": self.api,
			"NVDAObjects": nvdaObjects,
			"NVDAObjects.IAccessible": self.accessible,
			"windowUtils": self.windowUtils,
			"controlTypes": controlTypes,
			"winUser": winUser,
			"comtypes": comtypes,
			"logHandler": logHandler,
		}
		path = Path(__file__).resolve().parents[1] / "addon/globalPlugins/tonysEnhancements/status_bar.py"
		spec = importlib.util.spec_from_file_location("_status_bar_under_test", path)
		module = importlib.util.module_from_spec(spec)
		with patch.dict(sys.modules, dependencies):
			spec.loader.exec_module(module)
		self.enabled = True
		self.hook = module.StatusBarFallback(lambda: self.enabled)
		self.addCleanup(self.hook.terminate)

	def test_disabled_option_passes_through(self):
		self.enabled = False
		self.assertIsNone(self.api.getStatusBar())
		self.original.assert_called_once_with()
		self.api.getForegroundObject.assert_not_called()
		self.windowUtils.findDescendantWindow.assert_not_called()

	def test_existing_status_bar_is_preserved(self):
		self.original.return_value = self.statusBar
		self.assertIs(self.api.getStatusBar(), self.statusBar)
		self.api.getForegroundObject.assert_not_called()

	def test_fallback_finds_visible_native_status_bar(self):
		self.assertIs(self.api.getStatusBar(), self.statusBar)
		self.windowUtils.findDescendantWindow.assert_called_once_with(
			123, visible=True, className="msctls_statusbar32"
		)
		self.accessible.getNVDAObjectFromEvent.assert_called_once_with(456, -4, 0)

	def test_explicit_app_module_none_is_preserved(self):
		self.foreground.appModule = SimpleNamespace(statusBar=None)
		self.assertIsNone(self.api.getStatusBar())
		self.windowUtils.findDescendantWindow.assert_not_called()

	def test_checkbox_and_profile_changes_apply_immediately(self):
		self.enabled = False
		self.assertIsNone(self.api.getStatusBar())
		self.enabled = True
		self.assertIs(self.api.getStatusBar(), self.statusBar)
		self.enabled = False
		self.assertIsNone(self.api.getStatusBar())
		self.windowUtils.findDescendantWindow.assert_called_once()

	def test_missing_foreground_is_ignored(self):
		self.api.getForegroundObject.return_value = None
		self.assertIsNone(self.api.getStatusBar())
		self.windowUtils.findDescendantWindow.assert_not_called()

	def test_missing_window_handle_is_ignored(self):
		for foreground in (SimpleNamespace(), SimpleNamespace(windowHandle=0)):
			with self.subTest(foreground=foreground):
				self.api.getForegroundObject.return_value = foreground
				self.assertIsNone(self.api.getStatusBar())
		self.windowUtils.findDescendantWindow.assert_not_called()

	def test_no_visible_status_bar_returns_none(self):
		self.windowUtils.findDescendantWindow.side_effect = LookupError("No matching window")
		self.assertIsNone(self.api.getStatusBar())
		self.accessible.getNVDAObjectFromEvent.assert_not_called()

	def test_inaccessible_native_control_returns_none(self):
		self.accessible.getNVDAObjectFromEvent.return_value = None
		self.assertIsNone(self.api.getStatusBar())

	def test_native_control_must_have_status_bar_role(self):
		self.accessible.getNVDAObjectFromEvent.return_value = SimpleNamespace(role=1)
		self.assertIsNone(self.api.getStatusBar())

	def test_provider_errors_allow_normal_text_fallback(self):
		for error in (OSError("Window closed"), _COMError("Object disconnected")):
			with self.subTest(error=error):
				self.accessible.getNVDAObjectFromEvent.side_effect = error
				self.assertIsNone(self.api.getStatusBar())
		self.assertEqual(self.logger.debugWarning.call_count, 2)

	def test_original_errors_are_preserved(self):
		self.original.side_effect = RuntimeError("Original lookup failed")
		with self.assertRaisesRegex(RuntimeError, "Original lookup failed"):
			self.api.getStatusBar()

	def test_unload_restores_original_function(self):
		self.hook.terminate()
		self.assertIs(self.api.getStatusBar, self.original)
		self.hook.terminate()
		self.assertIs(self.api.getStatusBar, self.original)

	def test_unload_preserves_a_later_addon_wrapper(self):
		ourWrapper = self.api.getStatusBar

		def otherWrapper():
			return ourWrapper()

		self.api.getStatusBar = otherWrapper
		self.hook.terminate()
		self.assertIs(self.api.getStatusBar, otherWrapper)
		self.assertIsNone(self.api.getStatusBar())
		self.windowUtils.findDescendantWindow.assert_not_called()
