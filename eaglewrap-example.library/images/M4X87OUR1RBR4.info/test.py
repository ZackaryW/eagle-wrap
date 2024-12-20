

from eaglewrap.bridge import _applyCtx


ctx = _applyCtx()

ctx.api.applicationInfo()

print(f"selectedItems: {ctx.selectedItems}")
print(f"selectedFolders: {ctx.selectedFolders}")