from fluent_contents.extensions import plugin_pool, ContentPlugin
from .models import ProjectsBlockItem

@plugin_pool.register
class ProjectsBlockPlugin(ContentPlugin):
   model = ProjectsBlockItem
   render_template = "plugins/projectsblock.html"
   category = "Simple blocks"