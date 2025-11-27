/*
#	Java Les fondamentaux
#	A. Tasso
#	Carnet d'adresses
#	Fichier  : Adresses_View.java
*/

package CarnetModele;

import java.awt.Color;
import java.awt.Dimension;
import org.jdesktop.application.Action;
import org.jdesktop.application.ResourceMap;
import org.jdesktop.application.SingleFrameApplication;
import org.jdesktop.application.FrameView;
import org.jdesktop.application.TaskMonitor;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.BorderFactory;
import javax.swing.Timer;
import javax.swing.Icon;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.border.Border;

// La classe Adresses_View hérite des comportements d'une FrameView
public class Adresses_View extends FrameView {

    public Adresses_View(SingleFrameApplication app) {
         // Appeler le constructeur de la classe parente (de type FrameView)
        super(app);
          // Afficher les composants créés en mode Design
        initComponents();
        //  Créer un cadre orange
        cadre = BorderFactory.createLineBorder(Color.orange);
        // Récupérer l'adresse de la fenêtre principale
        JFrame mainFrame = Adresses_App.getApplication().getMainFrame();
        // La fenêtre de dialogue de saisie est créée en mémoire (mais non affichée)
         saisieDialog = new Saisie(mainFrame, true);
        // La boite de dialogue est positionnée relativement à la fenêtre principale
        saisieDialog.setLocationRelativeTo(mainFrame);

        // Intilaisation des contacts
        initContacts();

        // Code généré par NetBeans lors de la création d'une application de bureau
        // status bar initialization - message timeout, idle icon and busy animation, etc
        ResourceMap resourceMap = getResourceMap();
        int messageTimeout = resourceMap.getInteger("StatusBar.messageTimeout");
        messageTimer = new Timer(messageTimeout, new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                statusMessageLabel.setText("");
            }
        });
        messageTimer.setRepeats(false);
        int busyAnimationRate = resourceMap.getInteger("StatusBar.busyAnimationRate");
        for (int i = 0; i < busyIcons.length; i++) {
            busyIcons[i] = resourceMap.getIcon("StatusBar.busyIcons[" + i + "]");
        }
        busyIconTimer = new Timer(busyAnimationRate, new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                busyIconIndex = (busyIconIndex + 1) % busyIcons.length;
                statusAnimationLabel.setIcon(busyIcons[busyIconIndex]);
            }
        });
        idleIcon = resourceMap.getIcon("StatusBar.idleIcon");
        statusAnimationLabel.setIcon(idleIcon);
        progressBar.setVisible(false);

        // connecting action tasks to status bar via TaskMonitor
        TaskMonitor taskMonitor = new TaskMonitor(getApplication().getContext());
        taskMonitor.addPropertyChangeListener(new java.beans.PropertyChangeListener() {
            public void propertyChange(java.beans.PropertyChangeEvent evt) {
                String propertyName = evt.getPropertyName();
                if ("started".equals(propertyName)) {
                    if (!busyIconTimer.isRunning()) {
                        statusAnimationLabel.setIcon(busyIcons[0]);
                        busyIconIndex = 0;
                        busyIconTimer.start();
                    }
                    progressBar.setVisible(true);
                    progressBar.setIndeterminate(true);
                } else if ("done".equals(propertyName)) {
                    busyIconTimer.stop();
                    statusAnimationLabel.setIcon(idleIcon);
                    progressBar.setVisible(false);
                    progressBar.setValue(0);
                } else if ("message".equals(propertyName)) {
                    String text = (String)(evt.getNewValue());
                    statusMessageLabel.setText((text == null) ? "" : text);
                    messageTimer.restart();
                } else if ("progress".equals(propertyName)) {
                    int value = (Integer)(evt.getNewValue());
                    progressBar.setVisible(true);
                    progressBar.setIndeterminate(false);
                    progressBar.setValue(value);
                }
            }
        });
    }

    @Action
    // Afficher la boite AboutBox
    // Code généré par NetBeans lors de la création d'une application de bureau
    public void showAboutBox() {
        if (aboutBox == null) {
            JFrame mainFrame = Adresses_App.getApplication().getMainFrame();
            aboutBox = new Adresses_AboutBox(mainFrame);
            aboutBox.setLocationRelativeTo(mainFrame);
        }
        Adresses_App.getApplication().show(aboutBox);
    }

    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        mainPanel = new javax.swing.JPanel();
        boiteGlobale = new javax.swing.JPanel();
        boiteAvecScroll = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        boiteContacts = new javax.swing.JPanel();
        boiteInfos = new javax.swing.JPanel();
        menuBar = new javax.swing.JMenuBar();
        javax.swing.JMenu fileMenu = new javax.swing.JMenu();
        javax.swing.JMenuItem exitMenuItem = new javax.swing.JMenuItem();
        javax.swing.JMenu helpMenu = new javax.swing.JMenu();
        javax.swing.JMenuItem aboutMenuItem = new javax.swing.JMenuItem();
        statusPanel = new javax.swing.JPanel();
        javax.swing.JSeparator statusPanelSeparator = new javax.swing.JSeparator();
        statusMessageLabel = new javax.swing.JLabel();
        statusAnimationLabel = new javax.swing.JLabel();
        progressBar = new javax.swing.JProgressBar();
        plusBtn = new javax.swing.JButton();
        moinsBtn = new javax.swing.JButton();

        mainPanel.setName("mainPanel"); // NOI18N
        mainPanel.setLayout(new java.awt.BorderLayout());

        boiteGlobale.setName("boiteGlobale"); // NOI18N
        boiteGlobale.setLayout(new java.awt.GridLayout(1, 2));

        org.jdesktop.application.ResourceMap resourceMap = org.jdesktop.application.Application.getInstance(CarnetModele.Adresses_App.class).getContext().getResourceMap(Adresses_View.class);
        boiteAvecScroll.setBackground(resourceMap.getColor("boiteAvecScroll.background")); // NOI18N
        boiteAvecScroll.setBorder(javax.swing.BorderFactory.createTitledBorder(resourceMap.getString("boiteAvecScroll.border.title"))); // NOI18N
        boiteAvecScroll.setName("boiteAvecScroll"); // NOI18N
        boiteAvecScroll.setPreferredSize(new java.awt.Dimension(337, 500));

        jScrollPane1.setHorizontalScrollBarPolicy(javax.swing.ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
        jScrollPane1.setName("jScrollPane1"); // NOI18N

        boiteContacts.setName("boiteContacts"); // NOI18N

        org.jdesktop.layout.GroupLayout boiteContactsLayout = new org.jdesktop.layout.GroupLayout(boiteContacts);
        boiteContacts.setLayout(boiteContactsLayout);
        boiteContactsLayout.setHorizontalGroup(
            boiteContactsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(0, 664, Short.MAX_VALUE)
        );
        boiteContactsLayout.setVerticalGroup(
            boiteContactsLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(0, 558, Short.MAX_VALUE)
        );

        jScrollPane1.setViewportView(boiteContacts);

        org.jdesktop.layout.GroupLayout boiteAvecScrollLayout = new org.jdesktop.layout.GroupLayout(boiteAvecScroll);
        boiteAvecScroll.setLayout(boiteAvecScrollLayout);
        boiteAvecScrollLayout.setHorizontalGroup(
            boiteAvecScrollLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 335, Short.MAX_VALUE)
        );
        boiteAvecScrollLayout.setVerticalGroup(
            boiteAvecScrollLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(jScrollPane1, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 499, Short.MAX_VALUE)
        );

        boiteGlobale.add(boiteAvecScroll);

        boiteInfos.setBorder(javax.swing.BorderFactory.createTitledBorder(resourceMap.getString("boiteInfos.border.title"))); // NOI18N
        boiteInfos.setName("boiteInfos"); // NOI18N
        boiteInfos.setPreferredSize(new java.awt.Dimension(314, 500));
        boiteInfos.setLayout(new java.awt.BorderLayout());
        boiteGlobale.add(boiteInfos);

        mainPanel.add(boiteGlobale, java.awt.BorderLayout.CENTER);

        menuBar.setName("menuBar"); // NOI18N

        fileMenu.setText(resourceMap.getString("fileMenu.text")); // NOI18N
        fileMenu.setName("fileMenu"); // NOI18N

        javax.swing.ActionMap actionMap = org.jdesktop.application.Application.getInstance(CarnetModele.Adresses_App.class).getContext().getActionMap(Adresses_View.class, this);
        exitMenuItem.setAction(actionMap.get("quit")); // NOI18N
        exitMenuItem.setName("exitMenuItem"); // NOI18N
        fileMenu.add(exitMenuItem);

        menuBar.add(fileMenu);

        helpMenu.setText(resourceMap.getString("helpMenu.text")); // NOI18N
        helpMenu.setName("helpMenu"); // NOI18N

        aboutMenuItem.setAction(actionMap.get("showAboutBox")); // NOI18N
        aboutMenuItem.setAccelerator(javax.swing.KeyStroke.getKeyStroke(java.awt.event.KeyEvent.VK_I, java.awt.event.InputEvent.CTRL_MASK));
        aboutMenuItem.setName("aboutMenuItem"); // NOI18N
        helpMenu.add(aboutMenuItem);

        menuBar.add(helpMenu);

        statusPanel.setName("statusPanel"); // NOI18N

        statusPanelSeparator.setName("statusPanelSeparator"); // NOI18N

        statusMessageLabel.setName("statusMessageLabel"); // NOI18N

        statusAnimationLabel.setHorizontalAlignment(javax.swing.SwingConstants.LEFT);
        statusAnimationLabel.setName("statusAnimationLabel"); // NOI18N

        progressBar.setName("progressBar"); // NOI18N

        plusBtn.setText(resourceMap.getString("plusBtn.text")); // NOI18N
        plusBtn.setName("plusBtn"); // NOI18N
        plusBtn.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                plusBtnActionPerformed(evt);
            }
        });

        moinsBtn.setText(resourceMap.getString("moinsBtn.text")); // NOI18N
        moinsBtn.setName("moinsBtn"); // NOI18N
        moinsBtn.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                moinsBtnActionPerformed(evt);
            }
        });

        org.jdesktop.layout.GroupLayout statusPanelLayout = new org.jdesktop.layout.GroupLayout(statusPanel);
        statusPanel.setLayout(statusPanelLayout);
        statusPanelLayout.setHorizontalGroup(
            statusPanelLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(statusPanelSeparator, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, 695, Short.MAX_VALUE)
            .add(statusPanelLayout.createSequentialGroup()
                .addContainerGap()
                .add(plusBtn, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 54, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(moinsBtn, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 55, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .add(29, 29, 29)
                .add(statusMessageLabel)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 358, Short.MAX_VALUE)
                .add(progressBar, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED)
                .add(statusAnimationLabel)
                .addContainerGap())
        );
        statusPanelLayout.setVerticalGroup(
            statusPanelLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.LEADING)
            .add(statusPanelLayout.createSequentialGroup()
                .add(statusPanelSeparator, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, 2, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(org.jdesktop.layout.LayoutStyle.RELATED, 13, Short.MAX_VALUE)
                .add(statusPanelLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.TRAILING)
                    .add(statusPanelLayout.createSequentialGroup()
                        .add(statusPanelLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                            .add(statusMessageLabel)
                            .add(statusAnimationLabel)
                            .add(progressBar, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE, org.jdesktop.layout.GroupLayout.DEFAULT_SIZE, org.jdesktop.layout.GroupLayout.PREFERRED_SIZE))
                        .add(16, 16, 16))
                    .add(statusPanelLayout.createSequentialGroup()
                        .add(statusPanelLayout.createParallelGroup(org.jdesktop.layout.GroupLayout.BASELINE)
                            .add(plusBtn)
                            .add(moinsBtn))
                        .addContainerGap())))
        );

        setComponent(mainPanel);
        setMenuBar(menuBar);
        setStatusBar(statusPanel);
    }// </editor-fold>//GEN-END:initComponents
 // Actions à mener lorsque l'utilisateur clique sur le bouton +
    private void plusBtnActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_plusBtnActionPerformed
        // la boite de dialogue est affichée
        Adresses_App.getApplication().show(saisieDialog);
        // La saisie des données a été validé lorsque getDonnees() retourne true
        if (saisieDialog.getDonnees()){
              // Supprimer les composants de la boite de contacts
              boiteContacts.removeAll();
              // Mettre à jour la liste des contacts
              initContacts();
              // Afficher la  boite de contacts avec la nouvelle liste
              boiteContacts.validate();
        }
    }//GEN-LAST:event_plusBtnActionPerformed
    // Actions à mener lorsque l'utilisateur clique sur le bouton -
    private void moinsBtnActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_moinsBtnActionPerformed
        // Supprimer le contact dont le numéro correspond à celui qui a été sélectionné dans contactMouseReleased
        saisieDialog.supprimer(numero);
        // Supprimer les composants de la boite de contacts
        boiteContacts.removeAll();
        // Réafficher la boite de contacts
        boiteContacts.repaint();
        // Le contact sélectionné est le premier de la liste
        numero =0;
        // Mettre à jour la liste des contacts
        initContacts();
    }//GEN-LAST:event_moinsBtnActionPerformed
    // La mise à jour de la liste des contacts passe par la lecture du fichier listeContacts.txt
    private void  initContacts(){
              Dimension taille;
              String chaine;
              String [] info = new String[8];
              listeContacts = new Contact[50];
              // Ouvrir en lecture le fichier des contacts
              Fichier fic = new Fichier();
              fic.ouvrirEnLecture("../Donnees/listeContacts.txt");
              int i = 0;
              // Lire le fichier ...
              do{
                 // Stocker la ligne lue dans chaine
                 chaine = fic.lire();
                 // Si la chaine n'est pas vide
                 if (chaine != null) {
                    // Extraire les infos sous la forme d'un tableau contenant
                    // le nom, le prénom, ...
                    info = fic.extraireDonnees(chaine);
                    // Créer un contact à partir des données extraites
                    listeContacts[i]  = new Contact(info, i);
                    // Récupérer la taille du composant Contact
                    taille = listeContacts[i].getPreferredSize();
                    // Placer le contact en fonction de sa taille et de son indice dans la liste
                    listeContacts[i].setBounds(0, i*(taille.height+2), taille.width, taille.height);
                    // Ajouter le contact à la boite des contacts
                    boiteContacts.add(listeContacts[i]);
                    // Calculer la taihle de tous les composants + 1 (connaitre la hauteur)
                    taille.setSize(taille.width, (i+1)*(taille.height+2));
                    // Modifier la taille de la boite de contacts pour afficher une scrollbar, si nécessaire
                    boiteContacts.setPreferredSize(taille);
                    boiteContacts.validate();
                    // Ajouter l'écoute de l'événement mouseReleased
                    listeContacts[i].addMouseListener(new java.awt.event.MouseAdapter() {
                        @Override
                        public void mouseReleased(java.awt.event.MouseEvent evt) {
                             contactMouseReleased(evt);
                        }
                    });
                    i++;
                }
              // ... tant qu'il reste des lignes à lire
              } while (chaine != null);
              fic.fermer();
              // Afficher les infos relatives au contact d'indice 0
              boiteInfos.add(new Infos(listeContacts[0].getListeInfos())) ;
              // Afficher un cadre orange autour du contact d'indice 0
              listeContacts[0].setBorder(cadre);
              boiteInfos.validate();
    }

    // Sélectionner un élément de la liste de contacts
    private void contactMouseReleased(java.awt.event.MouseEvent evt) {
       // Mémoriser le numéro précédemment sélectionné pour effacer le cadre jaune qui l'entoure
       numeroPrec = numero;
       listeContacts[numeroPrec].setBorder(null);
       // Récupérer le contact sélectionné et son id
       Contact contatctSelectionne = (Contact) evt.getSource();
       numero = contatctSelectionne.getId();
       // Afficher les infos concernant le contact sélectionné dans la boite Infos
       boiteInfos.add(new Infos(listeContacts[numero].getListeInfos())) ;
       boiteInfos.validate();
       // Mettre un cadre jaune sur le contact sélectionné
       listeContacts[numero].setBorder(cadre);
    }


    // Variable de classe
    private Contact [] listeContacts;
    private Border cadre;
    private int numeroPrec = 0;
    private int numero = 0;
    private Saisie saisieDialog ;
    
    // Déclaration de variables créées par NetBeans par l'intermédiaire du mode Design 
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JPanel boiteAvecScroll;
    private javax.swing.JPanel boiteContacts;
    private javax.swing.JPanel boiteGlobale;
    private javax.swing.JPanel boiteInfos;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JPanel mainPanel;
    private javax.swing.JMenuBar menuBar;
    private javax.swing.JButton moinsBtn;
    private javax.swing.JButton plusBtn;
    private javax.swing.JProgressBar progressBar;
    private javax.swing.JLabel statusAnimationLabel;
    private javax.swing.JLabel statusMessageLabel;
    private javax.swing.JPanel statusPanel;
    // End of variables declaration//GEN-END:variables
    // Déclaration de variables créées par NetBeans  lors de la création d'une application de bureau
    private final Timer messageTimer;
    private final Timer busyIconTimer;
    private final Icon idleIcon;
    private final Icon[] busyIcons = new Icon[15];
    private int busyIconIndex = 0;
    private JDialog aboutBox;
}
