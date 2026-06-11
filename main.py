from pywinauto import Desktop
from pywinauto.keyboard import send_keys
import time


FACETS_TITLE = "Facets"
TARGET_TREE_ITEM = "Hospital Claims Processing"


def main():
    print("Connecting to FACETS...")

    # Attach to FACETS mother window
    facets = Desktop(backend="uia").window(
        title=FACETS_TITLE,
        control_type="Window"
    )

    facets.wait("exists visible enabled", timeout=15)
    facets.set_focus()
    time.sleep(0.5)

    print("FACETS found and focused.")

    # Find the tree item
    print(f"Looking for: {TARGET_TREE_ITEM}")

    item = facets.child_window(
        title_re=rf"^\s*{TARGET_TREE_ITEM}\s*$",
        control_type="TreeItem"
    )

    item.wait("exists visible enabled", timeout=15)

    print("Tree item found.")
    print("Name:", item.window_text())
    print("Rectangle:", item.rectangle())

    # First attempt: double click
    print("Double-clicking item...")
    item.double_click_input()
    time.sleep(1)

    print("Double-click done.")

    # Optional fallback:
    # If double-click does not open it, uncomment this block.
    """
    print("Trying fallback: click + Enter...")
    item.click_input()
    time.sleep(0.3)
    send_keys("{ENTER}")
    print("Fallback done.")
    """


if __name__ == "__main__":
    main()