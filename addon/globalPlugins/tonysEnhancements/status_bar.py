# A part of Tony's Enhancements add-on for NVDA.
# Copyright (C) 2026 Tony Malykh
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

"""Find native status bars missed by NVDA's position-based lookup."""

import api
import controlTypes
import NVDAObjects.IAccessible
import windowUtils
import winUser
from comtypes import COMError
from logHandler import log


class StatusBarFallback:
	def __init__(self, isEnabled):
		self._isEnabled = isEnabled
		self._active = True
		self._original = api.getStatusBar
		self._replacement = self._getStatusBar
		api.getStatusBar = self._replacement

	def _getStatusBar(self):
		status = self._original()
		if status is not None or not self._active or not self._isEnabled():
			return status
		foreground = api.getForegroundObject()
		windowHandle = getattr(foreground, "windowHandle", None)
		if not windowHandle:
			return None
		try:
			# An explicit app-module result of None requests display-text
			# fallback. Only use our lookup if no override is implemented.
			try:
				_ = foreground.appModule.statusBar
			except NotImplementedError:
				pass
			else:
				return None
			handle = windowUtils.findDescendantWindow(
				windowHandle,
				visible=True,
				className="msctls_statusbar32",
			)
			status = NVDAObjects.IAccessible.getNVDAObjectFromEvent(handle, winUser.OBJID_CLIENT, 0)
			if status and status.role == controlTypes.Role.STATUSBAR:
				return status
		except LookupError:
			pass
		except (COMError, OSError):
			log.debugWarning("Native status bar lookup failed", exc_info=True)
		return None

	def terminate(self):
		self._active = False
		# Another add-on may have wrapped us since installation. Leave its
		# wrapper in place; any remaining calls through ours now pass through.
		if api.getStatusBar is self._replacement:
			api.getStatusBar = self._original
