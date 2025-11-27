/*
#	Java Les fondamentaux
#	A. Tasso
#	Carnet d'adresses
#	Fichier  : Fichier.java
*/


package CarnetModele;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.StringTokenizer;

// La classe Fichier ne s'appuie pas sur un composant graphique pour fonctionner.
// Elle traite du stockage des données au sein de fichiers texte.
public class Fichier {

 // Propriétés de la classe
 private   BufferedWriter fW;
 private   BufferedReader fR;
 private   String urlFichier;

 // Méthode en set pour initialiser l'url d'accès au fichier à traiter
 public void setUrlFichier(String tmp){
      urlFichier = tmp;
 }
 // Ouvrir un fichier en lecture
 public boolean  ouvrirEnLecture(String nf) {
        // Essayer de réaliser les instructions suivantes :
        // Si aucune erreur n'est détectée, exécuter les instructions du bloc try
        // Sinon exécuter les instructions du bloc catch
	try {
            setUrlFichier(nf);
            File f = new File(urlFichier);
            // Création d'un flux en lecture ligne par ligne
	    fR  = new BufferedReader(new FileReader(f));
            fW = null;
            return true;
	}
        // Si une erreur est détéctée (le fichier n'existe pas, ...)
	catch (IOException e)	{
                // afficher le message d'erreur
                System.out.println(urlFichier+" : Erreur  à l'ouverture en lecture");
		return false;
	}
 }

 // Lire le flux en lecture ligne par ligne
 public String lire()  {
     // Essayer de réaliser les instructions suivantes :
     // Si aucune erreur n'est détectée, exécuter les instructions du bloc try
     // Sinon exécuter les instructions du bloc catch
     try {
         // Lire la ligne courante et la retourner au  programme appelant
	String chaine = fR.readLine();
	return chaine;
        }
        // Si une erreur est détéctée (le fichier n'est pas ouvert en lecture, ...)
	catch (IOException err) {
                 // afficher le message d'erreur
		System.out.println(urlFichier+" : Erreur  de lecture ");
                return null;
	}
 }

 // Découper les données d'une ligne
 public String [] extraireDonnees(String tmp)  {
    if (tmp != null) {
      // Créer un outil qui découpe  la chaine passée en paramètre (premier paramètre)
      // en utilisant le point-virgule (second paramètre) pour séparer les mots
      StringTokenizer st = new StringTokenizer(tmp,";");
      int i=0;
      // Créer un tableau à la taille du nombre de mots à extraire
      String mot[] = new String[st.countTokens()];
      // Parcourir l'ensemble des mots à extraire
      while (st.hasMoreTokens()) {
          // Les mémoriser dans un tableau
         mot[i] = st.nextToken();
         i++;
       }
       // Retourner le tableau contenant les mots extraits
       return mot;
     }
     else return null;
 }

 // Fermer le fichier ouvert en lecture ou en écriture
 public boolean fermer()  {
     // Essayer de réaliser les instructions suivantes :
     // Si aucune erreur n'est détectée, exécuter les instructions du bloc try
     // Sinon exécuter les instructions du bloc catch
     try {
       if (fR != null) fR.close();
       else  if (fW != null) fW.close();
       return true;
     }
      // Si une erreur est détéctée (le fichier n'existe pas, n'est pas ouvert, ...)
     catch (IOException err) {
         // afficher le message d'erreur
	System.out.println(urlFichier+" : Erreur  à la fermeture ");
        return false;
     }
 }
  // Ouvrir un fichier en écriture
  public boolean  ouvrirEnEcriture(String nf) {
        // Essayer de réaliser les instructions suivantes :
        // Si aucune erreur n'est détectée, exécuter les instructions du bloc try
        // Sinon exécuter les instructions du bloc catch
	try {
            setUrlFichier(nf);
            File f = new File(urlFichier);
             // Création d'un flux en écriture ligne par ligne
	    fW = new BufferedWriter(new FileWriter(f));
            fR = null;
            return true;
	}
         // Si une erreur est détéctée (le fichier n'existe pas, ...)
	catch (IOException e)	{
                // afficher le message d'erreur
                System.out.println(urlFichier+" : Erreur  à l'ouverture en écriture ");
		return false;
	}
 }

 // Ecrire dans le flux ouvert en écriture ligne par ligne, passer à la ligne 
 public boolean ecrire(String tmp) {
      // Essayer de réaliser les instructions suivantes :
      // Si aucune erreur n'est détectée, exécuter les instructions du bloc try
      // Sinon exécuter les instructions du bloc catch
      try {
 	if (tmp != null)   {
                // Ecrire lz chaine tmp du caractère 0 jusqu'à la fin du mot
		fW.write(tmp,0,tmp.length());
                // Passer à la ligne suivante
		fW.newLine();
	}
        return true;
        }
       // Si une erreur est détéctée (le fichier n'est pas ouvert en écriture
	catch (IOException err) {
                 // afficher le message d'erreur
		System.out.println(urlFichier+" : Erreur  d'écriture ");
                return false;
	}
   }
}


