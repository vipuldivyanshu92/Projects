/**
 * <p>Title: BlablaServeur</p>
 * <p>Company: Minosis.com</p>
 * <p>Date: 27/03/2005</p>
 * @author Minosis - Julien Defaut
 * @version 1.0
 */

import java.io.*;

//** Classe qui gère les commandes tappées dans la console **
// implémentation de l'interface Runnable (une des 2 méthodes pour créer un thread)
class Commandes implements Runnable
{
  BlablaServ _blablaServ; // pour utilisation des méthodes de la classe principale
  BufferedReader _in; // pour gestion du flux d'entrée (celui de la console)
  String _strCommande=""; // contiendra la commande tapée
  Thread _t; // contiendra le thread

  //** Constructeur : initialise les variables nécessaires **
  Commandes(BlablaServ blablaServ)
  {
    _blablaServ=blablaServ; // passage de local en global
    // le flux d'entrée de la console sera géré plus pratiquement dans un BufferedReader
    _in = new BufferedReader(new InputStreamReader(System.in));
    _t = new Thread(this); // instanciation du thread
    _t.start(); // demarrage du thread, la fonction run() est ici lancée
  }

  //** Methode : attend les commandes dans la console et exécute l'action demandée **
  public void run() // cette méthode doit obligatoirement être implémentée à cause de l'interface Runnable
  {
    try
    {
      // si aucune commande n'est tappée, on ne fait rien (bloquant sur _in.readLine())
      while ((_strCommande=_in.readLine())!=null)
      {
        if (_strCommande.equalsIgnoreCase("quit")) // commande "quit" detectée ...
          System.exit(0); // ... on ferme alors le serveur
        else if(_strCommande.equalsIgnoreCase("total")) // commande "total" detectée ...
        {
          // ... on affiche le nombre de clients actuellement connectés
          System.out.println("Nombre de connectes : "+_blablaServ.getNbClients());
          System.out.println("--------");
        }
        else
        {
          // si la commande n'est ni "total", ni "quit", on informe l'utilisateur et on lui donne une aide
          System.out.println("Cette commande n'est pas supportee");
          System.out.println("Quitter : \"quit\"");
          System.out.println("Nombre de connectes : \"total\"");
          System.out.println("--------");
        }
        System.out.flush(); // on affiche tout ce qui est en attente dans le flux
      }
    }
    catch (IOException e) {}
  }
}
