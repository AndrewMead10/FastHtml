# FastHtml

NOTE: Code is still being developed, expect all of this to be out of date

Inspired by [FastUI](https://github.com/pydantic/FastUI/tree/main), except we use regular html instead of react and we allow custom styling with tailwind css. Currently being developed and tested for use with fastAPI.

# Examples

```python

from components import (
    Heading,
    Button,
    Page,
    ComponentResponse,
    Text,
    NavBar,
    Dropdown,
    Slider,
    app,
)

@app.get("/custom-style")
def custom_style():
    heading = Heading(
        text="Hello World",
        level=2,
        custom_classes="flex justify-center items-center text-green-200",
    )
    return ComponentResponse(heading)


@app.get("/button-example")
def button_example():
    button = Button(text="Click Me", additional_classes="mt-4")
    return ComponentResponse(button)


@app.get("/page-example", response_class=ComponentResponse)
def page_example():
    heading = Heading(text="Welcome", level=1, additional_classes="text-red-500")
    button = Button(text="Get Started", additional_classes="mt-4")
    text = Text(text="this is some text")
    navbar = NavBar(
        title="My Site",
        items=[
            {"text": "Home", "href": "/"},
            {"text": "About", "href": "/button-example"},
            {"text": "Contact", "href": "/custom-style"},
        ],
    )

    dropdown_options = [
        {"value": "option1", "label": "Option 1"},
        {"value": "option2", "label": "A very long Option 2"},
        {"value": "option3", "label": "Option 3"},
    ]

    # Create a dropdown component
    dropdown = Dropdown(
        label="This is a dropdown", name="example_dropdown", options=dropdown_options
    )

    slider = Slider(
        name="volume",
        min_value=0,
        max_value=100,
        step=1,
        value=50,
        label="Volume Control:",
    )

    page = Page(
        title="Example Page",
        components=[navbar, heading, button, text, dropdown, slider],
    )
    return ComponentResponse(page)

```

# Features

`additional_classes:` Add tailind styles to the base component

`custom_style:` Override all styling for a component

# Current Components

```
Heading
Button
Page
Text
NavBar
Dropdown
Slider
```



