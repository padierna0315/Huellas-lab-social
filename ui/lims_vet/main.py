import flet as ft

def main(page: ft.Page):
    page.title = "LIMS Vet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    def route_change(route):
        page.views.clear()

        # Root View (Login / Role Selection)
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("LIMS Vet"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Select Role", size=24, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton("Admin Dashboard", on_click=lambda _: page.go("/admin")),
                                ft.ElevatedButton("Medico Dashboard", on_click=lambda _: page.go("/medico")),
                                ft.ElevatedButton("Auxiliar Dashboard", on_click=lambda _: page.go("/auxiliar")),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
            )
        )

        # Admin View
        if page.route == "/admin":
            page.views.append(
                ft.View(
                    "/admin",
                    [
                        ft.AppBar(title=ft.Text("Admin Dashboard"), bgcolor=ft.colors.BLUE_GREY),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Admin Operations", size=20),
                                    ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/")),
                                ]
                            ),
                            padding=20,
                        )
                    ],
                )
            )

        # Medico View
        elif page.route == "/medico":
            page.views.append(
                ft.View(
                    "/medico",
                    [
                        ft.AppBar(title=ft.Text("Medico Dashboard"), bgcolor=ft.colors.TEAL),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Medico Operations", size=20),
                                    ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/")),
                                ]
                            ),
                            padding=20,
                        )
                    ],
                )
            )

        # Auxiliar View
        elif page.route == "/auxiliar":
            page.views.append(
                ft.View(
                    "/auxiliar",
                    [
                        ft.AppBar(title=ft.Text("Auxiliar Dashboard"), bgcolor=ft.colors.INDIGO),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Auxiliar Operations", size=20),
                                    ft.ElevatedButton("Back to Home", on_click=lambda _: page.go("/")),
                                ]
                            ),
                            padding=20,
                        )
                    ],
                )
            )
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
