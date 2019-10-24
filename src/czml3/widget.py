from .core import Document, Preamble

CESIUM_TPL = """
<link rel="stylesheet" href="https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/Widgets/widgets.css" type="text/css">
<div id="cesiumContainer" style="width:100%; height:100%;"><div>
<script type="text/javascript">
{script}
</script>"""

SCRIPT_TPL = """
require.config({{
    paths: {{
        'cesium': 'https://cesium.com/downloads/cesiumjs/releases/{cesium_version}/Build/Cesium/Cesium'
    }}
}});

require(['cesium'], function (dependency) {{
    var czml = {czml};

    var viewer = new Cesium.Viewer('cesiumContainer', {{
        shouldAnimate : true
    }});

    // To have an inertial (ICRF) view
    function icrf(scene, time) {{
        var icrfToFixed = Cesium.Transforms.computeIcrfToFixedMatrix(time);
        if (Cesium.defined(icrfToFixed)) {{
            var camera = viewer.camera;
            var offset = Cesium.Cartesian3.clone(camera.position);
            var transform = Cesium.Matrix4.fromRotationTranslation(icrfToFixed);
            camera.lookAtTransform(transform, offset);
        }}
    }}
    // Temporarily disable inertial view
    // until we make it work with 2D Mercator view
    // and fix the zoom sensitivity, see
    // https://groups.google.com/d/msg/cesium-dev/vuXmepd4T2E/i71tq2I8EAAJ
    // viewer.scene.postUpdate.addEventListener(icrf);

    viewer.camera.flyHome(0);
    viewer.scene.globe.enableLighting = true;

    viewer.dataSources.add(Cesium.CzmlDataSource.load(czml));
}});
"""


class CZMLWidget:
    cesium_version = "1.62"

    def __init__(self, document=None):
        if document is not None:
            self._document = document
        else:
            self._document = Document([Preamble()])

    @property
    def document(self):
        return self._document

    def build_script(self):
        return SCRIPT_TPL.format(
            cesium_version=self.cesium_version, czml=self.document.dumps()
        )

    def to_html(self):
        return CESIUM_TPL.format(
            cesium_version=self.cesium_version, script=self.build_script()
        )

    def _repr_html_(self):
        return self.to_html()
