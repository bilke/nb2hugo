import os
from pathlib import Path
import shutil
from .exporter import HugoExporter


class HugoWriter:
    """A configurable writer to create Hugo markdown from a Jupyter notebook."""

    def __init__(self, config=None):
        self._exporter = HugoExporter(config)

    def convert(self, notebook, site_dir, section, template):
        """Convert a Jupyter notebook into a Hugo markdown and write
        the result in the content section of the site located in site_dir.
        """
        if template:
            self._exporter.template_paths.append(os.path.dirname(template))
            self._exporter.template_file = os.path.basename(template)

        (markdown, resources) = self._exporter.from_filename(notebook)
        self._write_resources_images(resources, site_dir, section)
        self._write_markdown(markdown, resources, site_dir, section)

    def _write_resources_images(self, resources, site_dir, section):
        """Process resources to create output images in the page bundle directory."""
        name = resources["metadata"]["name"].lower()
        target_dir = os.path.join(site_dir, "content", section, name)
        if "outputs" in resources:
            if resources["outputs"]:
                os.makedirs(target_dir, exist_ok=True)
            for key, value in resources["outputs"].items():
                target = os.path.join(target_dir, key)
                with open(target, "wb") as f:
                    f.write(value)
                    print(f"Created '{target}'")
        if "images_path" in resources:
            if resources["images_path"]:
                os.makedirs(target_dir, exist_ok=True)
            for key, value in resources["images_path"].items():
                target = os.path.join(target_dir, key)
                if Path(value).resolve() != Path(target).resolve():
                    shutil.copy2(value, target)
                    print(f"Created '{target}'")

    def _write_markdown(self, markdown, resources, site_dir, section):
        """Save markdown to file."""
        name = resources["metadata"]["name"].lower()
        target_dir = os.path.join(site_dir, "content", section, name)
        os.makedirs(target_dir, exist_ok=True)
        target = os.path.join(target_dir, "index.md")
        with open(target, "w") as f:
            f.write(markdown)
            print(f"Created '{target}'")
