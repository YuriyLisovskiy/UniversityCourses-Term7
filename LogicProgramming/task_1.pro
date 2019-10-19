male(robbie).
male(hart).
male(greg).
male(nikita).
female(kate).
female(monika).

% parent(MotherOrFather, Child).
parent(robbie, hart).
parent(robbie, greg).
parent(robbie, monika).
parent(nikita, hart).
parent(nikita, greg).
parent(nikita, monika).
parent(kate, nikita).
parent(corei, kate).

% rules
mother(Mother, Child) :- female(Mother), parent(Mother, Child).
father(Father, Child) :- male(Father), parent(Father, Child).

siblings(Person1, Person2) :-
	mother(Mother, Person1), mother(Mother, Person2),
	father(Father, Person1), father(Father, Person2),
	Person1 \= Person2.

brother(Brother, Child) :- siblings(Brother, Child), male(Brother).
sister(Sister, Child) :- siblings(Sister, Child), female(Sister).

descendent(Yong, Old) :-
	parent(Old, Yong), female(Yong);
	parent(Old, Yong), male(Yong).
descendent(Yong, Old) :- parent(Old, Parent), descendent(Yong, Parent).

ancestor(Old, Yong) :-
	parent(Old, Yong), female(Old);
	parent(Old, Yong), male(Old).
ancestor(Old, Yong) :- parent(Old, Parent), ancestor(Parent, Yong).

grandparent(GrandParent, GrandChild) :-
	parent(GrandParent, Parent),
	parent(Parent, GrandChild).

