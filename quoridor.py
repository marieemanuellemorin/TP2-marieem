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
class QuoridorError(Exception):
    pass


class Quoridor():
    
    def __init__(self, joueurs, murs):
        self.joueurs = joueurs
        self.murs = murs
        if type(self.joueurs) is list:
            if len(self.joueurs) != 2:
                raise QuoridorError('2 joueurs sont nécessaire pour initialiser une partie')
            elif type(self.joueurs[0]) is str and type(self.joueurs[1]) is str:
                namej1 = self.joueurs[0]
                positionj1 = (5,1)
                nbmur1 = 10
                namej2 = self.joueurs[1]
                positionj2 = (5,9)
                nbmur2 = 10
                self.joueurs = {"joueurs": [{"nom": namej1, "murs": nbmur1, "pos": positionj1},{"nom": namej2, "murs": nbmur2, "pos": positionj2}]}
            elif type(self.joueurs[0]) is dict and type(self.joueurs[1]) is dict:
                self.joueurs = {"joueurs": self.joueurs}
            else:
                raise QuoridorError('Joueurs doit soit être une liste de string, soit une liste de dictionnaires')
        else:
            raise QuoridorError('Joueurs doit être une liste')

    def déplacer_jeton(self, numero, position):
        self.numero = numero
        self.position = position
        if (self.numero != 1) and (self.numero != 2):
            raise QuoridorError("Le numéro du joueur doit soit être 1 ou 2")
        if self.position[0] < 1 or self.position[0] > 9 or self.position[1] < 1 or self.position[1] > 9:
            raise QuoridorError("La position désirée se trouve hors de la grille de jeu")
        else:
            graphe = construire_graphe([self.joueurs['joueurs'][0]['pos'],self.joueurs['joueurs'][1]['pos']],
            self.murs['horizontaux'],
            self.murs['verticaux'])
            deplacementadmissibles = list(graphe.successors(self.joueurs['joueurs'][self.numero-1]['pos']))
            dep = []
            for p in deplacementadmissibles:
                if self.position == p:
                    dep.append(p)
            if len(dep) == 1:
                self.joueurs['joueurs'][self.numero-1]['pos'] = self.position
            else:
                raise QuoridorError("Ce déplacement est invalide")
        
    def placer_mur(self, numero, position, orientation):
        self.numero = numero
        self.position = position
        self.orientation = orientation
        if self.numero != 1 and self.numero != 2:
            raise QuoridorError('Le numéro du joueur doit soit être 1 ou 2')
        elif self.orientation != 'horizontal' and self.orientation != 'vertical':
            raise QuoridorError("L'orientation du mur doit soit être 'horizontal' ou 'vertical'")
        elif type(self.position) is not tuple:
            raise QuoridorError('la coordonnée doit être entrée sous forme de tuple')
        elif len(self.position) != 2:
            raise QuoridorError('la coordonnée doit être de la forme (x, y)')
        elif self.joueurs['joueurs'][self.numero - 1]['murs'] == 0:
            raise QuoridorError('Il ne reste plus de murs disponibles à placer')
        # murs horizontaux
        elif self.orientation == 'horizontal':
            if self.position[0] < 1 or self.position[0] > 8 or self.position[1] < 2 or self.position[1] > 9:
                raise QuoridorError('La position désirée est hors de la grille de jeu')
            for h in self.murs['horizontaux']:
                if self.position == h:
                    raise QuoridorError('Un mur est déjà placé à cet endroit')
                elif self.position == (h[0]+1, h[1]):
                    raise QuoridorError('Un mur est déjà placé à cet endroit')
                elif self.position == (h[0]-1, h[1]):
                    raise QuoridorError('Un mur est déjà placé à cet endroit')
            for v in self.murs['verticaux']:
                if self.position == (v[0]-1, v[1]+1):
                    raise QuoridorError('Ce mur croiserait un mur vertical')
            self.murs['horizontaux'].append(position)
        # murs verticaux
        elif self.orientation == 'vertical':
            if self.position[0] < 2 or self.position[0] > 9 or self.position[1] < 1 or self.position[1] > 8:
                raise QuoridorError('La position désirée est hors de la grille de jeu')
            for v in self.murs['verticaux']:
                if self.position == v:
                    raise QuoridorError('Un mur est déjà placé à cet endroit')
                elif self.position == (h[0], h[1]+1):
                    raise QuoridorError('Un mur est déjà placé à cet endroit')
                elif self.position == (h[0], h[1]-1):
                    raise QuoridorError('Un mur est déjà placé à cet endroit')
            for h in self.murs['horizontaux']:
                if self.position == (h[0]+1, h[1]-1):
                    raise QuoridorError('Ce mur croiserait un mur horizontal')
            self.murs['verticaux'].append(position)
        self.joueurs['joueurs'][self.numero-1]['murs'] = self.joueurs['joueurs'][self.numero-1]['murs']-1

    def partie_terminée(self):
        graphe = construire_graphe([self.joueurs['joueurs'][0]['pos'],self.joueurs['joueurs'][1]['pos']],
            self.murs['horizontaux'],
            self.murs['verticaux'])
        if nx.has_path(graphe, self.joueurs['joueurs'][0]['pos'], 'B1') == False:
            return self.joueurs['joueurs'][1]['nom']
        if nx.has_path(graphe, self.joueurs['joueurs'][1]['pos'], 'B2') == False:
            return self.joueurs['joueurs'][0]['nom']
        if self.joueurs['joueurs'][0]['pos'][1] == 9:
            return self.joueurs['joueurs'][0]['nom']
        if self.joueurs['joueurs'][1]['pos'][1] == 1:
            return self.joueurs['joueurs'][1]['nom']
        return False

    def état_partie(self):
        état = dict(self.joueurs)
        self.murs = {"murs" : self.murs}
        état.update(self.murs)
        return état
        
    def __str__(self):
        position_idul = self.joueurs["joueurs"][0]["pos"]
        position_auto = self.joueurs["joueurs"][1]["pos"]
        murh = self.murs["horizontaux"]
        murv = self.murs["verticaux"]
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
        print(f'Légende: 1={self.joueurs["joueurs"][0]["nom"]}, 2={self.joueurs["joueurs"][1]["nom"]}')
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

    def jouer_coup(self, numero):
        graphe = construire_graphe([self.joueurs['joueurs'][0]['pos'],self.joueurs['joueurs'][1]['pos']],
            self.murs['horizontaux'],
            self.murs['verticaux'])
        self.numero = numero
        if self.numero != 1 and self.numero != 2:
            raise QuoridorError('Le numéro du joueur doit soit être 1 ou 2')
        chemin1 = nx.shortest_path(graphe, self.joueurs['joueurs'][0]['pos'], 'B1')
        chemin2 = nx.shortest_path(graphe, self.joueurs['joueurs'][1]['pos'], 'B2')
        if self.numero == 1:
            if self.joueurs['joueurs'][0]['murs'] == 0:
                self.déplacer_jeton(self.numero, chemin1[1])
                self.joueurs['joueurs'][self.numero-1]['pos'] = chemin1[1]
                return ('déplacer jeton', chemin1[1])
            else:
                if len(chemin2) >= 4:
                    self.déplacer_jeton(self.numero, chemin1[1])
                    self.joueurs['joueurs'][self.numero-1]['pos'] = chemin1[1]
                    return ('déplacer jeton', chemin1[1])
                else:
                    listepostesth = []
                    listepostestv = []
                    for x in range(1,9):
                        for y in range(1,9):
                            positiontest = (x, y)
                            for h in self.murs['horizontaux']:
                                if positiontest == h or positiontest == (h[0]+1, h[1]) or positiontest == (h[0]-1, h[1]):
                                    listepostesth = listepostesth
                                else:
                                     for v in self.murs['verticaux']:
                                        if positiontest == (v[0]-1, v[1]+1):
                                            listepostesth = listepostesth
                                        else:
                                            listepostesth.append(positiontest)
                            #murs vertical
                            for v in self.murs['verticaux']:
                                if positiontest == v or positiontest == (h[0], h[1]+1) or positiontest == (h[0], h[1]-1):
                                    listepostestv = listepostestv
                                else:
                                    for h in self.murs['horizontaux']:
                                        if positiontest == (h[0]+1, v[1]-1):
                                            listepostestv = listepostestv
                                        else:
                                            listepostestv.append(positiontest)
                    self.placer_mur(self.numero, listepostestv[0], 'vertical')
                    self.murs['verticaux'].append(listepostestv[0])
                    self.joueurs['joueurs'][self.numero-1]['murs'] = self.joueurs['joueurs'][self.numero-1]['murs']-1
                    return ('placer mur vertical', listepostestv[0])                   
        elif self.numero == 2:
            if self.joueurs['joueurs'][1]['murs'] == 0:
                self.déplacer_jeton(self.numero, chemin2[1])
                self.joueurs['joueurs'][self.numero-1]['pos'] = chemin2[1]
                return ('déplacer jeton', chemin2[1])
            else:
                if len(chemin1) >= 4:
                    self.déplacer_jeton(self.numero, chemin2[1])
                    self.joueurs['joueurs'][self.numero-1]['pos'] = chemin2[1]
                    return ('déplacer jeton', chemin2[1])
                else:
                    listepostesth = []
                    listepostestv = []
                    for x in range(1,9):
                        for y in range(1,9):
                            positiontest = (x, y)
                            for h in self.murs['horizontaux']:
                                if positiontest == h or positiontest == (h[0]+1, h[1]) or positiontest == (h[0]-1, h[1]):
                                    listepostesth = listepostesth
                                else:
                                     for v in self.murs['verticaux']:
                                        if positiontest == (v[0]-1, v[1]+1):
                                            listepostesth = listepostesth
                                        else:
                                            listepostesth.append(positiontest)
                            #murs vertical
                            for v in self.murs['verticaux']:
                                if positiontest == v or positiontest == (h[0], h[1]+1) or positiontest == (h[0], h[1]-1):
                                    listepostestv = listepostestv
                                else:
                                    for h in self.murs['horizontaux']:
                                        if positiontest == (h[0]+1, v[1]-1):
                                            listepostestv = listepostestv
                                        else:
                                            listepostestv.append(positiontest)
                    self.placer_mur(self.numero, listepostestv[0], 'vertical')
                    self.murs['verticaux'].append(listepostestv[0])
                    self.joueurs['joueurs'][self.numero-1]['murs'] = self.joueurs['joueurs'][self.numero-1]['murs']-1
                    return ('placer mur vertical', listepostestv[0])
