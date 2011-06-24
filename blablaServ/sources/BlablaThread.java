/**
 * <p>Title: BlablaServeur</p>
 * <p>Company: Minosis.com</p>
 * <p>Date: 27/03/2005</p>
 * @author Minosis - Julien Defaut
 * @version 1.0
 */

import java.net.*;
import java.io.*;

//** Classe associée à chaque client **
//** Il y aura autant d'instance de cette classe que de client connectés **
//implémentation de l'interface Runnable (une des 2 méthodes pour créer un thread)
class BlablaThread implements Runnable
{
  private Thread _t; // contiendra le thread du client
  private Socket _s; // recevra le socket liant au client
  private PrintWriter _out; // pour gestion du flux de sortie
  private BufferedReader _in; // pour gestion du flux d'entrée
  private BlablaServ _blablaServ; // pour utilisation des méthodes de la classe principale
  private int _numClient=0; // contiendra le numéro de client géré par ce thread

  //** Constructeur : crée les éléments nécessaires au dialogue avec le client **
  BlablaThread(Socket s, BlablaServ blablaServ) // le param s est donnée dans BlablaServ par ss.accept()
  {
    _blablaServ=blablaServ; // passage de local en global (pour gestion dans les autres méthodes)
    _s=s; // passage de local en global
    try
    {
      // fabrication d'une variable permettant l'utilisation du flux de sortie avec des string
      _out = new PrintWriter(_s.getOutputStream());
      // fabrication d'une variable permettant l'utilisation du flux d'entrée avec des string
      _in = new BufferedReader(new InputStreamReader(_s.getInputStream()));
      // ajoute le flux de sortie dans la liste et récupération de son numero
      _numClient = blablaServ.addClient(_out);
    }
    catch (IOException e){ }

    _t = new Thread(this); // instanciation du thread
    _t.start(); // demarrage du thread, la fonction run() est ici lancée
  }

  //** Methode :  exécutée au lancement du thread par t.start() **
  //** Elle attend les messages en provenance du serveur et les redirige **
  // cette méthode doit obligatoirement être implémentée à cause de l'interface Runnable
  public void run()
  {
    String message = ""; // déclaration de la variable qui recevra les messages du client
    // on indique dans la console la connection d'un nouveau client
    System.out.println("Un nouveau client s'est connecte, no "+_numClient);
    try
    {
      // la lecture des données entrantes se fait caractère par caractère ...
      // ... jusqu'à trouver un caractère de fin de chaine
      char charCur[] = new char[1]; // déclaration d'un tableau de char d'1 élement, _in.read() stockera y le char lu
      while(_in.read(charCur, 0, 1)!=-1) // attente en boucle des messages provenant du client (bloquant sur _in.read())
      {
      	// on regarde si on arrive à la fin d'une chaine ...
        if (charCur[0] != '\u0000' && charCur[0] != '\n' && charCur[0] != '\r')
                message += charCur[0]; // ... si non, on concatène le caractère dans le message
        else if(!message.equalsIgnoreCase("")) // juste une vérification de principe
        {
          if(charCur[0]=='\u0000') // le dernier caractère était '\u0000' (char de terminaison nulle)
          	// on envoi le message en disant qu'il faudra concaténer '\u0000' lors de l'envoi au client
            _blablaServ.sendAll(message,""+charCur[0]);
          else _blablaServ.sendAll(message,""); // sinon on envoi le message à tous
          message = ""; // on vide la chaine de message pour qu'elle soit réutilisée
        }
      }
    }
    catch (Exception e){ }
    finally // finally se produira le plus souvent lors de la deconnexion du client
    {
      try
      {
      	// on indique à la console la deconnexion du client
        System.out.println("Le client no "+_numClient+" s'est deconnecte");
        _blablaServ.delClient(_numClient); // on supprime le client de la liste
        _s.close(); // fermeture du socket si il ne l'a pas déjà été (à cause de l'exception levée plus haut)
      }
      catch (IOException e){ }
    }
  }
}
