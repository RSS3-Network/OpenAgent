import json

from loguru import logger
from playwright.sync_api import sync_playwright


class AccessibilityNavigator:
    def __init__(self):
        # Start Playwright and launch a browser
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.client = self.page.context.new_cdp_session(self.page)
        logger.info("Browser launched and new page created.")

    def goto(self, url):
        # Navigate to the specified URL and return the accessibility tree
        self.page.goto(url)
        ax_tree = self.page.accessibility.snapshot()
        logger.info(f"Navigated to {url} and captured accessibility tree.")
        return ax_tree

    def find_node_by_name_and_role(self, node, name, role):
        # Recursively search for a node with the specified name and role
        if node.get("name") == name and node.get("role") == role:
            return node
        if "children" in node:
            for child in node["children"]:
                result = self.find_node_by_name_and_role(child, name, role)
                if result:
                    return result
        return None

    def click(self, target_name, target_role):
        # Capture the current accessibility tree
        ax_tree = self.page.accessibility.snapshot()
        # Find the target node by name and role
        target_node = self.find_node_by_name_and_role(ax_tree, target_name, target_role)
        if target_node:
            logger.info(f"Found target node: {target_node}")

            # Get the document's nodeId
            document_node = self.client.send("DOM.getDocument")
            document_node_id = document_node["root"]["nodeId"]

            # Query the accessibility tree for the specific node information
            ax_query_result = self.client.send(
                "Accessibility.queryAXTree",
                {
                    "nodeId": document_node_id,
                    "accessibleName": target_name,
                    "role": target_role,
                },
            )

            # Get the backendNodeId of the element
            backend_node_id = ax_query_result["nodes"][0]["backendDOMNodeId"]

            # Get the bounding box of the element
            box_model = self.client.send("DOM.getBoxModel", {"backendNodeId": int(backend_node_id)})

            # Calculate the element's screen coordinates
            content_box = box_model["model"]["content"]
            x = content_box[0]
            y = content_box[1]

            logger.info(f"Element coordinates: x={x}, y={y}")

            # Simulate a mouse click at the calculated coordinates
            self.page.mouse.click(x, y)
            logger.info(f"Clicked on element with name '{target_name}' and role '{target_role}'.")

            # Wait for the page to load completely
            self.page.wait_for_load_state("networkidle")
            logger.info("Page load complete after click.")

    def close(self):
        # Close the browser and stop Playwright
        self.browser.close()
        self.playwright.stop()
        logger.info("Browser closed and Playwright stopped.")


# Usage example

if __name__ == "__main__":
    navigator = AccessibilityNavigator()
    ax_tree = navigator.goto("https://example.com")
    print(json.dumps(ax_tree, indent=2))

    navigator.click("More information...", "link")

    navigator.close()
