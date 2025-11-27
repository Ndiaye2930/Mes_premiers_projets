/*
#	Java Les fondamentaux
#	A. Tasso
#	Carnet d'adresses
#	Fichier  : Adresses_App.java
*/
package CarnetModele;

import org.jdesktop.application.Application;
import org.jdesktop.application.SingleFrameApplication;

/**
 * The main class of the application.
 */
// Code généré par NetBeans lors de la création d'une application de bureau
public class Adresses_App extends SingleFrameApplication {

    /**
     * At startup create and show the main frame of the application.
     */
    @Override protected void startup() {
        show(new Adresses_View(this));
    }

    /**
     * This method is to initialize the specified window by injecting resources.
     * Windows shown in our application come fully initialized from the GUI
     * builder, so this additional configuration is not needed.
     */
    @Override protected void configureWindow(java.awt.Window root) {
    }

    /**
     * A convenient static getter for the application instance.
     * @return the instance of Adresses_App
     */
    public static Adresses_App getApplication() {
        return Application.getInstance(Adresses_App.class);
    }

    /**
     * Main method launching the application.
     */
    public static void main(String[] args) {
        launch(Adresses_App.class, args);
    }
}
