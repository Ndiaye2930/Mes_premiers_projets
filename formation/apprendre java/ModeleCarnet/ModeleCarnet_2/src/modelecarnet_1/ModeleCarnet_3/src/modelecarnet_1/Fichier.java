/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package modelecarnet_1;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.StringTokenizer;

/**
 *
 * @author AnneT
 */
public class Fichier {


 private   BufferedWriter fW;
 private   BufferedReader fR;
 private   String urlFichier;

 public void setUrlFichier(String tmp){
      urlFichier = tmp;
 }
 // Ouvrir un fichier en lecture
 public boolean  ouvrirEnLecture(String nf) {
	try {
            setUrlFichier(nf);
            File f = new File(urlFichier);
	    fR  = new BufferedReader(new FileReader(f));
            fW = null;
            return true;
	}
	catch (IOException e)	{
                System.out.println(urlFichier+" : Erreur  à l'ouverture en lecture");
		return false;
	}
 }
 
 public String lire()  {
     try {
	String chaine = fR.readLine();
	return chaine;
        }
	catch (IOException err) { 
		System.out.println(urlFichier+" : Erreur  de lecture ");
                return null;
	}
 }


 public String [] extraireDonnees(String tmp)  {
    if (tmp != null) {
      StringTokenizer st = new StringTokenizer(tmp,";");
      int i=0;
      String mot[] = new String[st.countTokens()];
      while (st.hasMoreTokens()) {
         mot[i] = st.nextToken();
         i++;
       }
       return mot;
     }
     else return null;
 }


 public boolean fermer()  {
     try {
       if (fR != null) fR.close();
       else  if (fW != null) fW.close();
       return true;
     }
     catch (IOException err) {
	System.out.println(urlFichier+" : Erreur  à la fermeture ");
        return false;
     }
 }
  // Ouvrir un fichier en écriture
  public boolean  ouvrirEnEcriture(String nf) {
	try {
            setUrlFichier(nf);
            File f = new File(urlFichier);
	    fW = new BufferedWriter(new FileWriter(f));
            fR = null;
            return true;
	}
	catch (IOException e)	{
                System.out.println(urlFichier+" : Erreur  à l'ouverture en écriture ");
		return false;
	}
 }


 public boolean ecrire(String tmp) {
      try {
 	if (tmp != null)   {
		fW.write(tmp,0,tmp.length());
		fW.newLine();
	}
        return true;
        }
	catch (IOException err) {
		System.out.println(urlFichier+" : Erreur  d'écriture ");
                return false;
	}
   }
}


