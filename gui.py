from gui.controller import ApplicationController


if __name__ == "__main__":
    address_list = [
        ("ул. Пушкина, д. 1", 100, 200),
        ("пр. Ленина, д. 2", 150, 400),
        ("ул. Пушкина, д. 3", 440, 500),
        ("пр. Ленина, д. 4", 150, 700),
        ("ул. Пушкина, д. 5", 330, 100),
        ("пр. Ленина, д. 6", 230, 800)
    ]

    ants = 100
    iterations = 20
    alpha = 1.5
    beta = 1.2
    p = 0.6
    q = 10

    controller = ApplicationController(address_list, ants, iterations, alpha, beta, p, q)
    controller.run()
