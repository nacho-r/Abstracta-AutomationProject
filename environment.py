from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver_type = "CHROME"


def init_browser():
    if driver_type == "remote":
        return webdriver.Remote("http://192.168.1.3:4444/wd/hub", webdriver.DesiredCapabilities.CHROME)
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)


def before_scenario(context, scenario):
    print(f"scenario running: {scenario.name}")
    if "UI" in context.feature.tags:
        context.browser = init_browser()


def after_scenario(context, scenario):
    if context.failed and "web" in context.feature.tags:
        context.browser.save_screenshot(f"{scenario.name}.png")
        context.browser.quit()
