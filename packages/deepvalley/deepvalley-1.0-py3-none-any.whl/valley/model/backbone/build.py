from valley.utils import plugin
from .backbone import Backbone

def build_backbone(cfg, input_shape=None):
    """
    Build a backbone from `cfg.MODEL.BACKBONE.NAME`.

    Returns:
        an instance of :class:`Backbone`
    """
    #if input_shape is None:
    #    input_shape = ShapeSpec(channels=len(cfg.MODEL.PIXEL_MEAN))

    backbone_name = cfg.MODEL.BACKBONE.NAME

    backbone = plugin.get_plugin(plugin.PluginType.BACKBONE, backbone_name)(cfg, input_shape)

    assert isinstance(backbone, Backbone)
    return backbone