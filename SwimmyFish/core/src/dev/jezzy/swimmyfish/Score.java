package dev.jezzy.swimmyfish;

import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.graphics.g2d.Sprite;
import com.badlogic.gdx.graphics.g2d.TextureRegion;
import com.badlogic.gdx.scenes.scene2d.Actor;

import java.util.ArrayList;

public class Score extends Actor {
    private final SwimmyFish game;
    private final ArrayList<Sprite> digits;
    private final ArrayList<TextureRegion> numbers;
    private int score;

    public Score(SwimmyFish game) {
        this.game = game;
        numbers = new ArrayList<>();
        numbers.add(game.atlas.findRegion("zero"));
        numbers.add(game.atlas.findRegion("one"));
        numbers.add(game.atlas.findRegion("two"));
        numbers.add(game.atlas.findRegion("three"));
        numbers.add(game.atlas.findRegion("four"));
        numbers.add(game.atlas.findRegion("five"));
        numbers.add(game.atlas.findRegion("six"));
        numbers.add(game.atlas.findRegion("seven"));
        numbers.add(game.atlas.findRegion("eight"));
        numbers.add(game.atlas.findRegion("nine"));

        score = 0;
        digits = new ArrayList<>();
        Sprite newSprite = new Sprite(numbers.getFirst());
        digits.add(newSprite);
        setWidth(newSprite.getWidth());

        toFront();
    }

    public void update() {
        score++;
        ArrayList<Integer> newDigits = new ArrayList<>();
        int temp = score;
        while (temp > 0) {
            newDigits.addFirst(temp % 10);
            temp /= 10;
        }

        for (int i = 0; i < newDigits.size(); i++) {
            if (i >= digits.size()) {
                Sprite newSprite = new Sprite(numbers.get(newDigits.get(i)));
                digits.add(newSprite);
                setWidth(getWidth() + newSprite.getWidth());
            } else {
                digits.get(i).setRegion(numbers.get(newDigits.get(i)));
            }
        }
    }

    public void dispose() {}

    @Override
    public void draw(Batch batch, float ignoredParentAlpha) {
        float y = game.camera.position.y + (game.camera.viewportHeight / 2) -
                  numbers.getFirst().getRegionHeight() * 1.25f;
        float x = game.camera.position.x - getWidth() / 2f;

        for (int i = 0; i < digits.size(); i++) {
            digits.get(i).setPosition(x + i * digits.get(i).getWidth(), y);
            digits.get(i).draw(batch);
        }
    }
}
