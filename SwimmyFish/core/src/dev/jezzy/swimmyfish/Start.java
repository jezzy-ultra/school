package dev.jezzy.swimmyfish;

import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.scenes.scene2d.Group;
import com.badlogic.gdx.scenes.scene2d.actions.Actions;

public class Start extends Group {
    private final SwimmyFish game;
    private final CountdownCallback callback;
    private final TextureRegion three;
    private final TextureRegion two;
    private final TextureRegion one;
    private final Sprite sprite;

    public Start(SwimmyFish game, CountdownCallback callback) {
        this.game = game;
        this.callback = callback;
        three = game.atlas.findRegion("big three");
        two = game.atlas.findRegion("big two");
        one = game.atlas.findRegion("big one");

        sprite = new Sprite(three);
        act();
    }

    public void act() {
        this.addAction(
                Actions.sequence(Actions.run(() -> sprite.setRegion(three)),
                        Actions.fadeOut(1),

                        Actions.run(() -> sprite.setRegion(two)),
                        Actions.fadeIn(0), Actions.fadeOut(1),

                        Actions.run(() -> sprite.setRegion(one)),
                        Actions.fadeIn(0), Actions.fadeOut(1),

                        Actions.run(() -> {
                            callback.onFinish();
                            Start.this.remove();
                        })));
    }

    public void dispose() {}

    @Override
    public void draw(Batch batch, float parentAlpha) {
        sprite.setPosition(game.camera.position.x - sprite.getWidth() / 2f,
                game.camera.viewportHeight / 3);
        sprite.draw(batch);
    }
}
