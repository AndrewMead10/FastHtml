from jinja2 import Environment, FileSystemLoader
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response

app = FastAPI()

env = Environment(loader=FileSystemLoader("templates"))


class CacheControlStaticFiles(StaticFiles):
    def __init__(self, *args, **kwargs):
        self.cache_timeout = kwargs.pop("cache_timeout", 0)
        super().__init__(*args, **kwargs)

    async def get_response(self, path: str, scope) -> Response:
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = (
            f"max-age={self.cache_timeout}, must-revalidate"
        )
        return response


app.mount("/css", CacheControlStaticFiles(directory="css", cache_timeout=0), name="css")


class BaseComponent:
    def __init__(self, additional_classes="", custom_classes=""):
        self.additional_classes = additional_classes
        self.custom_classes = custom_classes
        self.html = self.render()

    def render(self):
        raise NotImplementedError("Subclasses must implement the render method")

    def get_classes(self, default_classes):
        if self.custom_classes:
            return self.custom_classes
        return f"{default_classes} {self.additional_classes}".strip()

    def __html__(self):
        return self.html


class ComponentResponse(HTMLResponse):
    def __init__(self, component: BaseComponent, **kwargs):
        content = component.__html__()
        super().__init__(content=content, **kwargs)


class Heading(BaseComponent):
    def __init__(self, text, level=1, additional_classes="", custom_classes=""):
        self.text = text
        self.level = level
        super().__init__(additional_classes, custom_classes)

    def render(self):
        classes = self.get_classes(self.default_classes())
        return f"<h{self.level} class='{classes}'>{self.text}</h{self.level}>"

    def default_classes(self):
        return "text-2xl font-bold"


class Button(BaseComponent):
    def __init__(self, text, additional_classes="", custom_classes=""):
        self.text = text
        super().__init__(additional_classes, custom_classes)

    def render(self):
        classes = self.get_classes(self.default_classes())
        return f"<button class='{classes}'>{self.text}</button>"

    def default_classes(self):
        return "bg-slate-500 hover:bg-slate-700 text-white font-bold py-2 px-3 rounded"


class Text(BaseComponent):
    def __init__(self, text, additional_classes="", custom_classes=""):
        self.text = text
        super().__init__(additional_classes, custom_classes)

    def render(self):
        classes = self.get_classes(self.default_classes())
        return f"<p class='{classes}'>{self.text}</p>"

    def default_classes(self):
        return "text-base text-lg"


class NavBar(BaseComponent):
    def __init__(self, title, items, additional_classes="", custom_classes=""):
        self.title = title
        self.items = items
        super().__init__(additional_classes, custom_classes)

    def render(self):
        classes = self.get_classes(self.default_classes())
        items_html = "".join(
            f"<li class='mr-6'><a class='text-slate-800 hover:text-slate-500' href='{item['href']}'>{item['text']}</a></li>"
            for item in self.items
        )
        return f"""
            <nav class='{classes}'>
                <div class='flex items-center'>
                    <a class='text-2xl font-semibold mr-6 text-slate-800' href='/'>{self.title}</a>
                    <ul class='flex'>{items_html}</ul>
                </div>
            </nav>
        """

    def default_classes(self):
        return "bg-white p-4 border-b border-slate-300"


class Dropdown(BaseComponent):
    def __init__(
        self, name, options, label="", additional_classes="", custom_classes=""
    ):
        self.name = name
        self.options = options
        self.label = label
        super().__init__(additional_classes, custom_classes)

    def render(self):
        classes = self.get_classes(self.default_classes())
        options_html = "".join(
            f"<option value='{option['value']}'>{option['label']}</option>"
            for option in self.options
        )
        label_html = (
            f"<label class='block text-lg font-semibold text-slate-800 mb-2'>{self.label}</label>"
            if self.label
            else ""
        )
        return f"""
            <div class='dropdown-component'>
                {label_html}
                <select name='{self.name}' class='{classes}'>
                    {options_html}
                </select>
            </div>
        """

    def default_classes(self):
        return "bg-white border border-slate-300 text-slate-800 px-3 py-2 rounded"


class Slider(BaseComponent):
    def __init__(
        self,
        name,
        min_value=0,
        max_value=100,
        step=1,
        value=50,
        label="",
        additional_classes="",
        custom_classes="",
    ):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        self.label = label
        super().__init__(additional_classes, custom_classes)

    def render(self):
        classes = self.get_classes(self.default_classes())
        label_html = (
            f"<label class='block text-lg font-semibold text-slate-700 mb-2'>{self.label}</label>"
            if self.label
            else ""
        )
        slider_id = f"slider_{self.name}"
        value_display_id = f"value_display_{self.name}"
        return f"""
            <div class='slider-component'>
                {label_html}
                <input type='range' id='{slider_id}' name='{self.name}' min='{self.min_value}' max='{self.max_value}' step='{self.step}' value='{self.value}' class='{classes}' oninput="document.getElementById('{value_display_id}').innerText = this.value">
                <span id='{value_display_id}' class='ml-2'>{self.value}</span>
            </div>
        """

    def default_classes(self):
        return "slider bg-slate-200 appearance-none rounded h-2"


class Page(BaseComponent):
    def __init__(
        self,
        template_name="base.html",
        title="",
        components=[BaseComponent],
        additional_classes="",
        custom_classes="",
    ):
        self.title = title
        self.components = components
        self.template_name = template_name
        super().__init__(additional_classes, custom_classes)

    def render(self):
        body_content = "".join(component.__html__() for component in self.components)
        template = env.get_template(self.template_name)
        return template.render(title=self.title, body=body_content)
