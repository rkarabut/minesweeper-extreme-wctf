winrt::build!(
    dependencies
        os
    types
        windows::foundation::numerics::{Vector2, Vector3}
        windows::foundation::TimeSpan
        windows::graphics::SizeInt32
        windows::system::DispatcherQueueController
        windows::ui::composition::{
            AnimationIterationBehavior,
            CompositionBatchTypes,
            CompositionBorderMode,
            CompositionColorBrush,
            CompositionGeometry,
            CompositionShape,
            CompositionSpriteShape,
            Compositor,
            ContainerVisual,
            SpriteVisual,
        }
        windows::ui::composition::desktop::DesktopWindowTarget
        windows::ui::core::{
            CoreDispatcher,
            CoreDispatcherPriority,
            CoreWindow,
            DispatchedHandler,
            IdleDispatchedHandler,
        }
        windows::ui::Colors
        windows::ui::xaml::controls::TextBlock
        windows::ui::xaml::hosting::ElementCompositionPreview
        windows::ui::xaml::Window
);

fn main() {
    build();
}
