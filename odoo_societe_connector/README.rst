=============
odoo_societe_connector
=============

`odoo_societe_connector` is an Odoo module that integrates Societe.com's API to enrich contact and company data within Odoo. It allows for automatic retrieval of legal and executive information for companies using data provided by Societe.com.

## Features

- **Company Enrichment**:
  - Automatically fills in company records with legal information such as VAT number, RCS, registration date, NAF code, address, and more.

- **Contact Enrichment**:
  - Adds or updates executive contacts associated with a company using information from Societe.com.

- **Easy Configuration**:
  - Configure the module by entering an authentication token from Societe.com in the company profile within Odoo.

## Installation

1. **Download the Module**:
   Download the module from the Odoo App Store or get it from a Git repository.

2. **Install the Module**:
   - Copy the `odoo_societe_connector` folder into your Odoo `addons` directory.
   - Restart the Odoo server.

   ```bash
   sudo systemctl restart odoo


### `README.rst` en français

=============
odoo_societe_connector
=============

`odoo_societe_connector` est un module Odoo qui intègre l'API de Societe.com pour enrichir les données des contacts et des sociétés dans Odoo. Il permet de récupérer automatiquement des informations légales et de dirigeants pour les sociétés en utilisant les données fournies par Societe.com.

## Fonctionnalités

- **Enrichissement des Sociétés** :
  - Complète automatiquement les champs d'une fiche société avec des informations légales telles que le numéro de TVA, le RCS, la date d'immatriculation, le code NAF, l'adresse, et plus encore.

- **Enrichissement des Contacts** :
  - Ajoute ou met à jour les contacts dirigeants associés à une société en utilisant les informations fournies par Societe.com.

- **Paramétrage Facile** :
  - Configurez le module en entrant un token d'authentification depuis le profil de la société dans Odoo.

## Installation

1. **Téléchargez le Module** :
   Téléchargez le module depuis l'App Store Odoo ou obtenez-le depuis un dépôt Git.

2. **Installation du Module** :
   - Copiez le dossier `odoo_societe_connector` dans le répertoire `addons` de votre installation Odoo.
   - Redémarrez le serveur Odoo.

   ```bash
   sudo systemctl restart odoo
