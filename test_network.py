from playwright.sync_api import Route, expect


def test_listen_network(page):
    page.on("request", lambda request: print(">>", request.method, request.url))
    page.on("response", lambda response: print("<<", response.status, response.url))
    page.goto("https://yandex.ru/")


def test_network(page):
    page.route("**/register", lambda route: route.continue_(post_data='{"email": "eve.holt@reqres.in","password": "pistol"}'))
    page.goto('https://reqres.in/')
    page.get_by_text(' Register - successful ').click()


def test_mock_tags(page):
    page.route("**/api/tags", lambda route: route.fulfill(path="data/data.json"))
    page.goto("https://demo.realworld.io/")

def test_intercepted(page):
    def handle_route(route: Route):
        response = route.fetch()
        json = response.json()
        json["tags"] = ["Первый", "Второй"]
        route.fulfill(json=json)

    page.route("**/api/tags", handle_route)

    page.goto("https://demo.realworld.io/")
    sidebar = page.locator('css=div.sidebar')
    expect(sidebar.get_by_role('link')).to_contain_text(["Первый", "Второй"])


def test_inventory(page):
    response = page.request.get('https://petstore.swagger.io/v2/store/inventory')
    print(response.status)
    print(response.json())


def test_add_user(page):
    data = [
              {
                "id": 9743,
                "username": "fsd",
                "firstName": "fff",
                "lastName": "ggg",
                "email": "bbb",
                "password": "tt",
                "phone": "333",
                "userStatus": 0
              }
            ]
    header = {
        'accept': 'application/json',
        'content-Type': 'application/json'
    }
    response = page.request.post('https://petstore.swagger.io/v2/user/createWithArray',data=data, headers=header)
    print(response.status)
    print(response.json())

    