/**
 * <p>Title: BlablaServeur</p>
 * <p>Company: Minosis.com</p>
 * <p>Date: 27/03/2005</p>
 * @author Minosis - Julien Defaut
 * @version 1.0
 */

import java.net.*;
import java.io.*;
import java.util.*;

//** Classe principale du serveur, gère les infos globales **
public class BlablaServ
{
  private Vector _tabClients = new Vector(); // contiendra tous les flux de sortie vers les clients
  private int _nbClients=0; // nombre total de clients connectés

  //** Methode : la première méthode exécutée, elle attend les connections **
  public static void main(String args[])
  {
    BlablaServ blablaServ = new BlablaServ(); // instance de la classe principale
    try
    {
      Integer port;
      if(args.length<=0) port=new Integer("18000"); // si pas d'arguments : port 18000 par défaut
      else port = new Integer(args[0]); // sinon il s'agit du buméro de port passé en argument

      new Commandes(blablaServ); // lance le thread de gestion des commandes

      ServerSocket ss = new ServerSocket(port.intValue()); // ouverture d'un socket serveur sur port
      printWelcome(port);
      while (true) // attente en boucle de connexion (bloquant sur ss.accept)
      {
        new BlablaThread(ss.accept(),blablaServ); // un client se connecte, un nouveau thread client est lancé
      }
    }
    catch (Exception e) { }
  }

  //** Methode : affiche le message d'accueil **
  static private void printWelcome(Integer port)
  {
    System.out.println("--------");
    System.out.println("BlablaServeur : Par Minosis - Julien Defaut - 2005");
    System.out.println("Derniere version : 27/03/2005");
    System.out.println("--------");
    System.out.println("Demarre sur le port : "+port.toString());
    System.out.println("--------");
    System.out.println("Quitter : tapez \"quit\"");
    System.out.println("Nombre de connectes : tapez \"total\"");
    System.out.println("--------");
  }


  //** Methode : envoie le message à tous les clients **
  synchronized public void sendAll(String message,String sLast)
  {
    PrintWriter out; // declaration d'une variable permettant l'envoie de texte vers le client
    for (int i = 0; i < _tabClients.size(); i++) // parcours de la table des connectés
    {
      out = (PrintWriter) _tabClients.elementAt(i); // extraction de l'élément courant (type PrintWriter)
      if (out != null) // sécurité, l'élément ne doit pas être vide
      {
      	// ecriture du texte passé en paramètre (et concaténation d'ue string de fin de chaine si besoin)
        out.print(message+sLast);
        out.flush(); // envoi dans le flux de sortie
      }
    }
  }

  //** Methode : détruit le client no i **
  synchronized public void delClient(int i)
  {
    _nbClients--; // un client en moins ! snif
    if (_tabClients.elementAt(i) != null) // l'élément existe ...
    {
      _tabClients.removeElementAt(i); // ... on le supprime
    }
  }

  //** Methode : ajoute un nouveau client dans la liste **
  synchronized public int addClient(PrintWriter out)
  {
    _nbClients++; // un client en plus ! ouaaaih
    _tabClients.addElement(out); // on ajoute le nouveau flux de sortie au tableau
    return _tabClients.size()-1; // on retourne le numéro du client ajouté (size-1)
  }

  //** Methode : retourne le nombre de clients connectés **
  synchronized public int getNbClients()
  {
    return _nbClients; // retourne le nombre de clients connectés
  }

}
