import re
import sys
import time

from pywinauto import Desktop
from pywinauto.keyboard import send_keys


FACETS_TITLE = "Facets"
TARGET_TREE_ITEM = "Hospital Claims Processing"
TIMEOUT_SECONDS = 15


def list_visible_window_titles(desktop):
    print("Visible window titles:")
    found_title = False

    for window in desktop.windows(visible_only=True):
        try:
            title = window.window_text().strip()
        except Exception:
            continue

        if title:
            found_title = True
            print(f"  - {title!r}")

    if not found_title:
        print("  (No titled visible windows found.)")


def dump_visible_tree_items(facets):
    print("Visible TreeItem names under FACETS:")
    found_item = False

    try:
        tree_items = facets.descendants(control_type="TreeItem")
    except Exception as exc:
        print(f"  Unable to enumerate TreeItems: {exc}")
        return

    for tree_item in tree_items:
        try:
            if tree_item.is_visible():
                found_item = True
                print(f"  - {tree_item.window_text()!r}")
        except Exception:
            continue

    if not found_item:
        print("  (No visible TreeItems found.)")


def main():
    print("Starting FACETS proof-of-concept click test.")
    print('Connecting to the FACETS window using Desktop(backend="uia")...')
    desktop = Desktop(backend="uia")
    facets = desktop.window(title=FACETS_TITLE, control_type="Window")

    try:
        facets.wait("exists visible enabled", timeout=TIMEOUT_SECONDS)
    except Exception as exc:
        print(
            f"ERROR: FACETS window {FACETS_TITLE!r} was not found, visible, "
            f"and enabled within {TIMEOUT_SECONDS} seconds."
        )
        print(f"Details: {exc}")
        list_visible_window_titles(desktop)
        return 1

    print("FACETS window found. Setting focus...")
    try:
        facets.set_focus()
        time.sleep(0.5)
    except Exception as exc:
        print(f"ERROR: Could not focus the FACETS window: {exc}")
        return 1

    target_pattern = rf"^\s*{re.escape(TARGET_TREE_ITEM)}\s*$"
    print(f"Searching for TreeItem matching {target_pattern!r}...")
    item = facets.child_window(title_re=target_pattern, control_type="TreeItem")

    try:
        item.wait("exists visible enabled", timeout=TIMEOUT_SECONDS)
        item_wrapper = item.wrapper_object()
    except Exception as exc:
        print(
            f"ERROR: TreeItem {TARGET_TREE_ITEM!r} was not found, visible, "
            f"and enabled within {TIMEOUT_SECONDS} seconds."
        )
        print(f"Details: {exc}")
        dump_visible_tree_items(facets)
        return 1

    print(f"Found item name: {item_wrapper.window_text()!r}")
    print(f"Found item rectangle: {item_wrapper.rectangle()}")

    try:
        print("Double-clicking the TreeItem...")
        item_wrapper.double_click_input()
        print("Double-click completed.")
    except Exception as double_click_error:
        print(f"Double-click failed: {double_click_error}")
        print("Trying fallback: click the TreeItem, then send Enter...")
        try:
            item_wrapper.click_input()
            time.sleep(0.3)
            send_keys("{ENTER}")
            print("Fallback click + Enter completed.")
        except Exception as fallback_error:
            print(f"ERROR: Fallback click + Enter failed: {fallback_error}")
            return 1

    print("FACETS proof-of-concept click test finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
