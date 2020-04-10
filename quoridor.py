import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Construire un graphe de la grille.

    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.

    Args:
        joueurs (list): une liste des positions (x,y) des joueurs.
        murs_horizontaux (list): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (list): une liste des positions (x,y) des murs verticaux.

    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe

    état = {
    "joueurs": [
        {"nom": namej1, "murs": nbmur1, "pos": positionj1},
        {"nom": namej2, "murs": nbmur2, "pos": positionj2}
    ],
    "murs": {
        "horizontaux": [(4, 4), (2, 6), (3, 8), (5, 8), (7, 8)],
        "verticaux": [(6, 2), (4, 4), (2, 5), (7, 5), (7, 7)]
    }
}

class Quoridor():
    
    def __init__(self, joueurs, murs):
        self.joueurs = joueurs
        self.murs = murs
        if self.joueurs[0] == str:
            namej1 = self.joueurs[0]
            positionj1 = (5,1)
            nbmur1 = 10
            namej2 = self.joueurs[1]
            positionj2 = (5,9)
            nbmur2 = 10
            self.joueurs = {"joueurs": [{"nom": namej1, "murs": nbmur1, "pos": positionj1},{"nom": namej2, "murs": nbmur2, "pos": positionj2}]}
        elif self.joueurs[0] == dict:
            self.joueurs = joueurs
        else:
            raise QuoridorError
        
            

    def déplacer_jeton(self, numero, position):
        self.numero = numero
        self.position = position
        if self.numero != 1 or self.numero != 2:
            raise QuoridorError
        elif self.position[0] < 1 or self.position[0] > 9 or self.position[1] < 1 or self.position[1] > 9:
            raise QuoridorError
        else:
            graphe = construire_graphe([self.joueurs['pos'] for j in self.joueurs['joueurs']], 
            self.murs['murs']['horizontaux'],
            self.murs['murs']['verticaux'])
            deplacementadmissibles = list(graphe.successors(self.joueurs[numero-1]['pos']))
            for p in deplacementadmissibles:
                if p == self.position:
                    self.joueurs[numero-1]['pos'] = self.position
                else:
                    raise QuoridorError
        
    def placer_mur(self, numero, position, orientation):
        self.numero = numero
        self.position = position
        self.orientation = orientation
        if self.numero != '1' or self.numero != '2':
            raise QuoridorError
        elif self.orientation != 'horizontal' or self.orientation != 'vertical':
            raise QuoridorError
        elif self.position != tuple:
            raise QuoridorError
        elif self.joueurs['murs'] == 0:
            raise QuoridorError
        # murs horizontaux
        elif self.orientation == 'horizontal':
            for h in self.murs['horizontaux']:
                if self.position == h:
                    raise QuoridorError
                elif self.position == (h[0]+1, h[1]):
                    raise QuoridorError
                elif self.position == (h[0]-1, h[1]):
                    raise QuoridorError
                elif self.position[0] > 8:
                    raise QuoridorError
            for v in self.murs['verticaux']:
                if self.position == (v[0]-1, v[1]+1):
                    raise QuoridorError
            self.murs['horizontaux'].append(position)
        # murs verticaux
        elif self.orientation == 'vertical':
            for v in self.murs['verticaux']:
                if self.position == v:
                    raise QuoridorError
                elif self.position == (h[0], h[1]+1):
                    raise QuoridorError
                elif self.position == (h[0], h[1]-1):
                    raise QuoridorError
                elif self.position[1] > 8:
                    raise QuoridorError
            for v in self.murs['verticaux']:
                if self.position == (v[0]+1, v[1]+1):
                    raise QuoridorError
            self.murs['verticaux'].append(position)
        self.joueurs[self.numero-1]['murs'] = self.joueurs[self.numero-1]['murs']-1

    def partie_terminée(self):
        if nx.has_path(graphe, self.joueurs[0]['pos'], 'B1') == False:
            return self.joueurs[1]['nom']
        if nx.has_path(graphe, self.joueurs[1]['pos'], 'B2') == False:
            return self.joueurs[0]['nom']
        if self.joueurs[0]['pos'][1] == 9:
            return self.joueurs[0]['nom']
        if self.joueurs[1]['pos'][1] == 1:
            return self.joueurs[1]
        return False

    def état_partie(self):
        état = dict(self.joueurs)
        état.update(self.murs)
        return état
        
    def __str__(self, état):
        self.état = état
        position_idul = self.état["joueurs"][0]["pos"]
        position_auto = self.état["joueurs"][1]["pos"]
        murh = self.état["murs"]["horizontaux"]
        murv = self.état["murs"]["verticaux"]
        lhead1 = '   -----------------------------------'
        lfoot1 = '--|-----------------------------------'
        lfoot2 = '  | 1   2   3   4   5   6   7   8   9 '
        vdebut = ' |'
        hdebut = '  |'
        full = [[' . '] * 9, [' . '] * 9, [' . '] * 9, [' . '] * 9, [' . '] * 9, [' . '] * 9, [' . '] * 9, [' . '] * 9, [' . '] * 9]
        half = [['   '] * 9, ['   '] * 9, ['   '] * 9, ['   '] * 9, ['   '] * 9, ['   '] * 9, ['   '] * 9, ['   '] * 9, ['   '] * 9]
        full[position_idul[1]-1][position_idul[0]-1] = ' 1 '
        #AUTOMATE
        full[position_auto[1]-1][position_auto[0]-1] = ' 2 '
        #MUR VERTICAL
        l = len(murv)
        for i in range(l):
            full[murv[i][1]-1][murv[i][0]-1] = '| . '
            half[murv[i][1]][murv[i][0]-1] = '|   '
            full[murv[i][1]][murv[i][0]-1] = '| . '
        #MUR HORIZONTAL
        l = len(murh)
        for i in range(l):
            if half[murh[i][1]-1][murh[i][0]-1] == '|   ':
                half[murh[i][1]-1][murh[i][0]-1] = '|---'
            else:
                half[murh[i][1]-1][murh[i][0]-1] = '---'
            half[murh[i][1]-1][murh[i][0]] = '----'
        #AFFICHER TABLEAU
        print(f'Légende: 1={self.état["joueurs"][0]["nom"]}, 2={self.état["joueurs"][1]["nom"]}')
        print(lhead1)
        for y in range(9, 0, -1):
            lignefull= f'{y}' + vdebut
            lignehalf = hdebut
            for x in range(1, 10):
                if (len(f'{full[y-1][x-1]}') == 3) and (x > 1):
                    lignefull += ' '
                lignefull += f'{full[y-1][x-1]}'
                if (len(f'{half[y-1][x-1]}') == 3) and (x > 1):
                    lignehalf += ' '
                lignehalf += f'{half[y-1][x-1]}'
            lignefull += '|'
            lignehalf += '|'
            print(lignefull)
            if y > 1:
                print(lignehalf)
        print(lfoot1)
        print(lfoot2)
