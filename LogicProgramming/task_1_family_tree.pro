male(xavier).	  % 1st generation

male(darren).	  % 2nd generation

male(henry).	  % 3rd generation
male(ronald).	  % 3rd generation

male(ted).	  % 4th generation
male(dexter).	  % 4th generation
male(caleb).	  % 4th generation

male(alan).	  % 5th generation
male(bernard).	  % 5th generation

female(louisa).	  % 2nd generation
female(patricia). % 2nd generation

female(isabelle). % 3rd generation

female(caroline). % 4th generation
female(ashley).	  % 4th generation
female(alice).	  % 4th generation

female(eva).	  % 5th generation
female(annabel).  % 5th generation

% parent(MotherOrFather, Child).
parent(louisa, xavier).
parent(darren, xavier).

parent(isabelle, patricia).
parent(henry, patricia).
parent(isabelle, louisa).
parent(henry, louisa).

parent(ted, isabelle).
parent(caroline, isabelle).
parent(caleb, henry).
parent(alice, henry).
parent(caleb, ronald).
parent(alice, ronald).

parent(alan, ted).
parent(eva, ted).
parent(bernard, caroline).
parent(annabel, caroline).
parent(bernard, dexter).
parent(annabel, dexter).
parent(bernard, ashley).
parent(annabel, ashley).

% rules
mother(Mother, Child) :- female(Mother), parent(Mother, Child).
father(Father, Child) :- male(Father), parent(Father, Child).

siblings(Person1, Person2) :-
    mother(Mother, Person1), mother(Mother, Person2),
	father(Father, Person1), father(Father, Person2),
	Person1 \= Person2.

brother(Brother, Child) :- siblings(Brother, Child), male(Brother).
sister(Sister, Child) :- siblings(Sister, Child), female(Sister).

descendant(Young, Old) :-
	parent(Old, Young), female(Young);
	parent(Old, Young), male(Young).
descendant(Young, Old) :- parent(Old, Parent), descendant(Young, Parent).

ancestor(Old, Young) :-
	parent(Old, Young), female(Old);
	parent(Old, Young), male(Old).
ancestor(Old, Young) :- parent(Old, Parent), ancestor(Parent, Young).

grandparent(GrandParent, GrandChild) :-
	parent(GrandParent, Parent),
	parent(Parent, GrandChild).

uncle(Uncle, Person) :-
	mother(Mother, Person), brother(Uncle, Mother);
	father(Father, Person), brother(Uncle, Father).

aunt(Aunt, Person) :-
	mother(Mother, Person), sister(Aunt, Mother);
	father(Father, Person), sister(Aunt, Father).

