# L.E.U. DEPLOYMENT GUIDE (GitHub Pages & Smart Contracts)

Ce guide vous explique comment mettre votre site en ligne et déployer votre contrat intelligent, étape par étape.

## PARTIE 1 : Mettre le site en ligne (GitHub Pages)
1. Allez sur votre dépôt GitHub (`lingua-executabilis-universalis`).
2. Cliquez sur l'onglet **Settings** (en haut à droite).
3. Dans le menu de gauche, cliquez sur **Pages**.
4. Sous "Build and deployment", section "Branch", sélectionnez **`main`** et laissez **`/ (root)`**.
5. Cliquez sur **Save**.
6. Attendez 2 minutes. Actualisez la page "Pages". GitHub vous donnera une URL du type :
   `https://alpha0az1omega-sketch.github.io/lingua-executabilis-universalis/10_ASSETS/index.html`

## PARTIE 2 : Déployer le Smart Contract (Polygon)
1. Allez sur [Remix IDE](https://remix.ethereum.org).
2. Créez un nouveau fichier `LEU_Genesis_Pass.sol` et collez le code de votre contrat (dans `02_MVP/LEU_Genesis_Pass.sol`).
3. Allez dans l'onglet "Solidity Compiler" et compilez (version 0.8.0 ou plus).
4. Allez dans l'onglet "Deploy & Run Transactions".
5. Changez "Environment" pour "Injected Provider - MetaMask" (assurez-vous d'être sur le réseau Polygon).
6. Cliquez sur "Deploy".
7. Confirmez la transaction dans MetaMask. Votre contrat est déployé !

## PARTIE 3 : Uploader les iNFTs (OpenSea / IPFS)
1. Allez sur [Pinata Cloud](https://pinata.cloud) (gratuit jusqu'à 1 Go).
2. Uploadez le dossier `10_ASSETS/nft_metadata/` et le dossier `04_ARTIFACTS/primitives_3d/`.
3. Remplacez les `PLACEHOLDER_CID` dans les fichiers JSON par le vrai CID IPFS fourni par Pinata.
4. Sur OpenSea (Polygon), importez votre contrat et mintissez les 20 iNFTs en utilisant ces fichiers JSON.
