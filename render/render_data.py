from jinja2 import Environment, FileSystemLoader


def render_template(template_path, data):
    env = Environment(loader=FileSystemLoader('.'))

    template = env.get_template(template_path)

    return template.render(data)
