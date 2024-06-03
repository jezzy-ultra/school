package dev.jezzy.swimmyfish;

import com.badlogic.gdx.backends.lwjgl3.Lwjgl3Application;
import com.badlogic.gdx.backends.lwjgl3.Lwjgl3ApplicationConfiguration;

import static dev.jezzy.swimmyfish.SwimmyFish.WORLD_HEIGHT;
import static dev.jezzy.swimmyfish.SwimmyFish.WORLD_WIDTH;

public class DesktopLauncher {
    public static void main(String[] arg) {
        Lwjgl3ApplicationConfiguration config =
                new Lwjgl3ApplicationConfiguration();
        config.setTitle("Swimmy Fish");
        config.setWindowedMode(WORLD_WIDTH, WORLD_HEIGHT);
        config.setResizable(false);
        config.setForegroundFPS(144);
        config.useVsync(true);
        new Lwjgl3Application(new SwimmyFish(), config);
    }
}
