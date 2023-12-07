from typing import Literal
from PIL import Image


from invokeai.app.services.image_records.image_records_common import ImageCategory, ResourceOrigin
from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    InputField,
    invocation,
    invocation_output,
    OutputField,
    InvocationContext,
    WithMetadata,
    WithWorkflow,
)

from invokeai.app.invocations.primitives import (
    ImageField
)


@invocation_output("remove_background_output")
class RemoveBackgroundOutput(BaseInvocationOutput):
    image: ImageField = OutputField(description="The output image")
    mask: ImageField = OutputField(description="The output image mask")
    width: int = OutputField(description="The width of the image in pixels")
    height: int = OutputField(description="The height of the image in pixels")


MODELS_RM_BG = Literal[
    "u2net",
    "u2netp",
    "u2net_cloth_seg",
    "u2net_human_seg",
    "isnet-anime",
    "isnet-general-use",
    "silueta"
]

@invocation(
    "remove_background",
    title="Remove Background",
    tags=["image", "clipseg"],
    category="image",
    version="1.0.0",
)
class RemoveBackgroundInvocation(BaseInvocation, WithMetadata, WithWorkflow):
    """Tool to remove images background."""
    image: ImageField = InputField(default=None, description="Image to remove background from")
    model: MODELS_RM_BG = InputField(default="u2net", description="Model to use to remove background")
    alpha_matting: bool = InputField(default=False, description="Flag indicating whether to use alpha matting")
    alpha_matting_foreground_threshold: int = InputField(default=240, description="Foreground threshold for alpha matting")
    alpha_matting_background_threshold: int = InputField(default=10, description="Background threshold for alpha matting")
    alpha_matting_erode_size: int = InputField(default=10, description="Erosion size for alpha matting")
    post_process_mask: bool = InputField(default=False, description="Flag indicating whether to post-process the masks")

    def invoke(self, context: InvocationContext) -> RemoveBackgroundOutput:
        image = context.services.images.get_pil_image(self.image.image_name)

        try:
            from rembg import new_session, remove
            session = new_session(
                model_name=self.model
            )
            image_out = remove(
                data = image, 
                session=session,
                alpha_matting = self.alpha_matting,
                alpha_matting_foreground_threshold = self.alpha_matting_foreground_threshold,
                alpha_matting_background_threshold = self.alpha_matting_background_threshold,
                alpha_matting_erode_size = self.alpha_matting_erode_size,
                post_process_mask = self.post_process_mask,
            )
        except ImportError:
            context.services.logger.warning(
                "Remove Background --> To use this node, please quit InvokeAI and execute 'pip install rembg'"
            )
            context.services.logger.warning(
                "Remove Background --> rembg package not found. Passing through unaltered image!"
            )


        if self.model == "u2net_cloth_seg":
            image_out = self.combine_three_parts(image_out)

        image_dto = context.services.images.create(
            image=image_out,
            image_origin=ResourceOrigin.INTERNAL,
            image_category=ImageCategory.GENERAL,
            node_id=self.id,
            session_id=context.graph_execution_state_id,
            is_intermediate=self.is_intermediate,
            workflow=self.workflow,
        )


        image_mask = image_out.split()[3]

        image_mask_dto = context.services.images.create(
            image=image_mask,
            image_origin=ResourceOrigin.INTERNAL,
            image_category=ImageCategory.GENERAL,
            node_id=self.id,
            session_id=context.graph_execution_state_id,
            is_intermediate=self.is_intermediate,
            workflow=self.workflow,
        )

        return RemoveBackgroundOutput(
            image=ImageField(image_name=image_dto.image_name),
            mask=ImageField(image_name=image_mask_dto.image_name),
            width=image_dto.width,
            height=image_dto.height,
        )


    def combine_three_parts(self, image):
        images = []
        width, height = image.size
        part_height = height // 3
        for part in range(3):
            top = part * part_height
            bottom = (part + 1) * part_height
            images.append(image.crop((0, top, width, bottom)))
            
        out_image = images[0]
        for img in images[1:]:
            out_image = Image.alpha_composite(out_image, img)

        return out_image