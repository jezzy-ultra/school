package dev.jezzy.swimmyfish;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.audio.Sound;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.math.Circle;
import com.badlogic.gdx.scenes.scene2d.Actor;

public class PlayerFish extends Actor {
    private static final float GRAVITY = -1050;
    private final SwimmyFish game;
    private final TextureRegion region;
    private final Sound swimSound;
    private int movementSpeed;
    private float yVelocity;

    public PlayerFish(SwimmyFish game) {
        this.game = game;
        region = game.atlas.findRegion("player fish");
        setBounds(region.getRegionWidth() * 2,
                  game.camera.viewportHeight - region.getRegionY() / 2f, region.getRegionWidth(),
                  region.getRegionHeight());
        setOrigin(getWidth() / 2, getHeight() / 2);
        swimSound = Gdx.audio.newSound(Gdx.files.internal("swim.wav"));

        movementSpeed = 200;
        yVelocity = 0;
    }

    public Circle getBounds() {
        float radius = Math.min(getWidth(), getHeight()) / 2;
        radius -= 8; // make collision a bit more forgiving
        float centerX = getX() + getWidth() / 2;
        float centerY = getY() + getHeight() / 2;
        return new Circle(centerX, centerY, radius);
    }

    public void increaseSpeed() {
        movementSpeed += 2;
    }

    public void update(float deltaTime) {
        move(deltaTime);
    }

    private void move(float deltaTime) {
        setX(getX() + movementSpeed * deltaTime);
        setY(getY() + (yVelocity + deltaTime * GRAVITY / 2) * deltaTime);
        yVelocity += GRAVITY * deltaTime;

        int terminalVelocity = -850;
        if (yVelocity < terminalVelocity) {
            yVelocity = terminalVelocity;
        }
        if (getY() > game.viewport.getWorldHeight() - 75) {
            yVelocity *= 0.25f * deltaTime;
        }
    }

    public void jump() {
        yVelocity = 460;
        swimSound.play();
    }

    public void dispose() {
        swimSound.dispose();
    }

    @Override
    public void draw(Batch batch, float ignoredParentAlpha) {
        batch.draw(region, getX(), getY(), getOriginX(), getOriginY(), getWidth(), getHeight(),
                   getScaleX(), getScaleY(), getRotation());
    }
}
