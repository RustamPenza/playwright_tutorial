import pytest
import os
from playwright.sync_api import Playwright, sync_playwright, expect


def test_add_todo(page):
    page.goto("https://demo.playwright.dev/todomvc/#/")
    page.get_by_placeholder("What needs to be done?").click()
    page.get_by_placeholder("What needs to be done?").fill("Hellow world")
    page.get_by_placeholder("What needs to be done?").press("Enter")


def test_chexbox(page):
    page.goto("https://zimaev.github.io/checks-radios/")
    page.locator("text=Default checkbox").check()
    page.locator("text=Checked checkbox").check()
    page.locator("text=Default radio").check()
    page.locator("text=Default checked radio").check()
    page.locator("text=Checked switch checkbox input").check()


def test_select(page):
    page.goto("https://zimaev.github.io/select/")
    page.select_option("#floatingSelect", value="3")
    page.select_option("#floatingSelect", index=1)
    page.select_option("#floatingSelect", label="Нашел и завел bug")  # выбор по текстовому значению

    page.select_option("#skills", value=["docker", "python"])


def test_drag_and_drop(page):
    page.goto("https://zimaev.github.io/draganddrop/")
    page.drag_and_drop("#drag", "#drop")

def test_dialog(page):
    page.goto("https://zimaev.github.io/dialog/")
    page.on("dialog", lambda dialog: dialog.accept())  # dismiss() нажать отмена
    page.get_by_text("Диалог Confirmation").click()


def test_input_file(page):
    page.goto("https://zimaev.github.io/upload/")
    page.set_input_files("#formFile", "hello.txt")
    page.locator("#file-submit").click()


def test_download(page):

    page.goto("https://demoqa.com/upload-download")

    with page.expect_download() as download_info:
        page.locator("a:has-text(\"Download\")").click()

    download = download_info.value
    file_name = download.suggested_filename
    destination_folder_path = "./data/"
    download.save_as(os.path.join(destination_folder_path, file_name))


def test_new_tab(page):
    page.goto("https://zimaev.github.io/tabs/")
    with page.context.expect_page() as tab:
        page.get_by_text("Переход к Dashboard").click()

    new_tab = tab.value
    assert new_tab.url == "https://zimaev.github.io/tabs/dashboard/index.html?"
    sign_out = new_tab.locator(".nav-link", has_text="Sign out")
    assert sign_out.is_visible()


def test_assert(page):
    page.goto("https://demo.playwright.dev/todomvc/#/")
    expect(page).to_have_url("https://demo.playwright.dev/todomvc/#/")

    input_field = page.get_by_placeholder('What needs to be done?')
    expect(input_field).to_be_empty()

    input_field.fill("Task 1")
    input_field.press("Enter")

    input_field.fill("Task 2")
    input_field.press("Enter")

    todo_items = page.get_by_test_id("todo-item")
    expect(todo_items).to_have_count(2)

    todo_items.get_by_role("checkbox").nth(0).click()
    expect(todo_items.nth(0)).to_have_class("completed")

