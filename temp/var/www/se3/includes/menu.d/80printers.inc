<?php

   /**
   * Menu Imprimantes
  
   * @Version $Id: 80printers.inc 3670 2009-04-16 07:30:05Z gnumdk $
   
   * @Projet LCS / SambaEdu 
   
   * @Auteurs Equipe TICE crdp de Caen
   
   * @Note: 

   * @Licence Distribue sous la licence GPL
   */

   /**

   * file: 80printers.inc
   * @Repertoire: includes/menu.d/ 
   */  
  
require_once("lang.inc.php");
bindtextdomain('se3-core',"/var/www/se3/locale");
textdomain ('se3-core');

$liens1=array(array(
              gettext("Imprimantes"),"printers_is_admin",1,
              gettext("Gestion des imprimantes"),"printers/view_printers.php","se3_is_admin",1,
              gettext("Nouvelle imprimante"),"printers/config_printer.php","se3_is_admin",2,
              gettext("Ajout &#224; un parc"),"printers/add_printer.php","se3_is_admin",2,
              gettext("Suppression"),"printers/delete_printer_choice.php","se3_is_admin",2,
              gettext("Imprimante par defaut"),"printers/default_printer.php","se3_is_admin",2,
              gettext("Liste des imprimantes"),"printers/list_printers.php","printers_is_admin",1,
              gettext("Info serveur CUPS"),"printers/server_CUPS.php","se3_is_admin",1,
      ));
$liens=array_merge($liens,$liens1);
?>
