% ticket(
% 	TrainNumber,
% 	DepartingStation -> station(...),
% 	ArrivingStation -> station(...),
% 	CabNumber,
% 	SeatNumber
% )
ticket(1, station(lviv, _, _), station(rivne, _, _), 1, 2).
ticket(1, station(lviv, _, _), station(rivne, _, _), 1, 4).
ticket(3, station(lviv, _, _), station(kyiv, _, _), 1, 4).

% train(Number, Name, [Stations], [Cabs]).
train(
    1,
    "Rivne-Kyiv",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(rivne, "2019-03-04T10:00Z", "2019-03-04T10:00Z"),
        station(st4, "2019-03-04T12:10Z", "2019-03-04T12:20Z"),
        station(kyiv, "2019-03-04T13:40Z", "2019-03-04T13:40Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(3, coupe, 55, [3,4,5]),
        cab(4, open, 25, [5,6,7])
    ]
).
train(
    2,
    "Dnipro-Kyiv",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(dnipro, "2019-03-04T17:30Z", "2019-03-04T17:30Z"),
        station(kyiv, "2019-03-04T23:20Z", "2019-03-04T23:20Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(2, coupe, 55, [1,2]),
        cab(1, coupe, 55, [3,5])
    ]
).
train(
    3,
    "Lviv-Kyiv",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(lviv, "2019-03-04T13:00Z", "2019-03-04T13:00Z"),
        station(st2, "2019-03-04T14:30Z", "2019-03-04T14:40Z"),
        station(st5, "2019-03-04T15:30Z", "2019-03-04T15:40Z"),
        station(ternopil, "2019-03-04T16:50Z", "2019-03-04T17:00Z"),
        station(kyiv, "2019-03-04T18:40Z", "2019-03-04T18:40Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(1, coupe, 55, [3,4,5]),
        cab(3, open, 25, [5,6,7])
    ]
).
train(
    4,
    "Lviv-Rivne",
    [
    	% station(Name, ArrivalTime, DepartureTime).
    	station(kyiv, "2019-03-04T12:30Z", "2019-03-04T12:30Z"),
        station(st2, "2019-03-04T14:30Z", "2019-03-04T14:40Z"),
        station(st3, "2019-03-04T14:30Z", "2019-03-04T14:40Z"),
        station(rivne, "2019-03-04T16:40Z", "2019-03-04T16:40Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(1, coupe, 50, [1,2,3,4]),
        cab(2, open, 20, [5,6,7])
    ]
).
train(
    5,
    "Lviv-Ternopil",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(lviv, "2019-03-04T01:30Z", "2019-03-04T01:30Z"),
        station(st2, "2019-03-04T02:00Z", "2019-03-04T02:10Z"),
        station(st4, "2019-03-04T14:30Z", "2019-03-04T14:40Z"),
        station(ternopil, "2019-03-04T15:00Z", "2019-03-04T15:00Z")
    ],
    [
        % cab(Number, Type, PricePerSeat, [SeatNumbers]). 	
        cab(1, coupe, 55, [1,2,3]),
        cab(2, open, 25, [4,10]),
        cab(3, coupe, 55, [3,4,5]),
        cab(4, open, 25, [5,6,7])
    ]
).
train(
    6,
    "Kharkiv-Kyiv",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(kharkiv, "2019-03-04T17:30Z", "2019-03-04T17:30Z"),
        station(st7, "2019-03-04T19:00Z", "2019-03-04T19:10Z"),
        station(st6, "2019-03-04T21:10Z", "2019-03-04T21:20Z"),
        station(kyiv, "2019-03-04T23:20Z", "2019-03-04T23:20Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(2, coupe, 55, [1,2]),
        cab(1, coupe, 55, [3,5])
    ]
).
train(
    7,
    "Kyiv-Donetsk",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(kyiv, "2019-03-04T06:00", "2019-03-04T06:00Z"),
        station(st5, "2019-03-04T08:40Z", "2019-03-04T08:50Z"),
        station(st6, "2019-03-04T11:30Z", "2019-03-04T11:40Z"),
        station(donetsk, "2019-03-04T16:40Z", "2019-03-04T16:40Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(2, coupe, 55, [3,4,5]),
        cab(3, open, 25, [5,6,7])
    ]
).
train(
    8,
    "Mukachevo-Kharkiv",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(mukachevo, "2019-03-04T10:30Z", "2019-03-04T10:30Z"),
        station(st5, "2019-03-04T11:30Z", "2019-03-04T11:40Z"),
        station(st4, "2019-03-04T13:00Z", "2019-03-04T13:10Z"),
        station(st6, "2019-03-04T15:20Z", "2019-03-04T15:30Z"),
        station(kharkiv, "2019-03-04T16:40Z", "2019-03-04T16:40Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(3, coupe, 55, [3,4,5]),
        cab(4, open, 25, [5,6,7]),
        cab(2, coupe, 55, [1,2])
    ]
).
train(
    9,
    "Kyiv-Mukachevo",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(kyiv, "2019-03-04T09:10Z", "2019-03-04T09:10Z"),
        station(st6, "2019-03-04T12:00Z", "2019-03-04T12:10Z"),
        station(mukachevo, "2019-03-04T14:20Z", "2019-03-04T14:20Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(4, open, 25, [5,6,7]),
	    cab(2, coupe, 55, [1,2])
    ]
).
train(
    10,
    "Uzhgorod-Lviv",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(uzhgorod, "2019-03-04T07:30Z", "2019-03-04T07:30Z"),
        station(st1, "2019-03-04T09:00Z", "2019-03-04T09:10Z"),
        station(st2, "2019-03-04T10:20Z", "2019-03-04T10:30Z"),
        station(lviv, "2019-03-04T12:20Z", "2019-03-04T12:20Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(3, coupe, 55, [3,4,5]),
        cab(4, open, 25, [5,6,7])
    ]
).
train(
    11,
    "Uzhgorod-Rivne",
    [
    	% station(Name, ArrivalTime, DepartureTime).
        station(uzhgorod, "2019-03-04T06:30Z", "2019-03-04T06:30Z"),
        station(st1, "2019-03-04T08:00Z", "2019-03-04T08:10Z"),
        station(st2, "2019-03-04T09:30Z", "2019-03-04T09:40Z"),
        station(st4, "2019-03-04T10:50Z", "2019-03-04T11:00Z"),
        station(rivne, "2019-03-04T13:40Z", "2019-03-04T13:40Z")
    ],
    [
    	% cab(Number, Type, PricePerSeat, [SeatNumbers]).
        cab(1, coupe, 55, [3,4,5]),
        cab(5, open, 25, [5,6,7])
    ]
).

% get_train_number(Train -> Train(...), Number).
get_train_number(train(Number, _, _, _), Number).

% get_stations_by_train(Train -> Train(...), Stations -> out).
get_stations_by_train(train(Number, Name, Stations, Cabs), Stations) :- 
    train(Number, Name, Stations, Cabs).

% get_station_name(Station -> station(...), Name -> out)
get_station_name(station(Name, _, _), Name).

% Get parsed station departure time.
% 
% get_station_departure_time(Station -> station(...), DepartureTime -> out)
get_station_departure_time(station(_, _, Departure), DepartureTime):-
    parse_time(Departure, DepartureTime).

% Get parsed station arrival time.
% 
% get_station_arrival_time(Station -> station(...), ArrivalTime -> out)
get_station_arrival_time(station(_, Arrival, _), ArrivalTime):-
    parse_time(Arrival, ArrivalTime).

% Get station arrival time as string.
% 
% get_station_arrival_time_raw(Station -> station(...), Arrival -> out)
get_station_arrival_time_raw(station(_, Arrival, _), Arrival).


% Get AvailablePlaces in a train with TrainNumber from station with name From 
% to station with name To as a list of cabs without occupied places
% 
% Example:
% available_places_from_to_by_train(station(lviv, _, _), station(rivne, _, _), 1, X).
% 
% available_places_from_to_by_train(
% 	From -> station(...),
% 	To -> station(...),
% 	TrainNumber,
% 	AvailableCabs -> out
% ).
available_places_from_to_by_train(From, To, TrainNumber, AvailableCabs) :-
    train(TrainNumber, _, _, Cabs),
    cabs_without_occupied_places_from_to(TrainNumber, From, To, Cabs, AvailableCabs).

% End recursion
cabs_without_occupied_places_from_to(_, _, _, [], CabsOut) :- CabsOut = [].

cabs_without_occupied_places_from_to(TrainNumber, From, To, [CurrentCab | OtherCabs], CabsOut) :-
    cabs_without_occupied_places_from_to(TrainNumber, From, To, OtherCabs, OtherCabsOut),
    CurrentCab = cab(CabNumber, Type, Price, AllPlaces),
    available_places_from_to(TrainNumber, CabNumber, From, To, AllPlaces, AvailablePlaces),
    CabsOut = [cab(CabNumber, Type, Price, AvailablePlaces) | OtherCabsOut].

% End recursion
available_places_from_to(_, _, _, _, [], AvailablePlaces) :- AvailablePlaces = [].

available_places_from_to(TrainNumber, CabNumber, From, To, [CurrentPlace | OtherPlaces], AvailablePlaces) :-
	% Check place availability for each place in cab
    available_places_from_to(TrainNumber, CabNumber, From, To, OtherPlaces, OtherAvailablePlaces),
    
    % Get path part for this specific train in the general transit path
    train(TrainNumber, _, Stations, _),
    From = station(FromName, _, _),
    To = station(ToName, _, _),
    index_of(Stations, station(FromName, _, _), FromIndex),
    index_of(Stations, station(ToName, _, _), ToIndex),
    sublist(Path, FromIndex, ToIndex + 1, Stations),
    
 	% Check if a ticket occupies a place for a part of the path
 	% except for the beginning and the end of the path
 	% If it does - do not include the place
 	% Otherwise - include the place
    (
    	ticket(TrainNumber, TicketFrom, TicketTo, CabNumber, CurrentPlace),
        check_ticket_intersection(TrainNumber, TicketFrom, TicketTo, Path, Result),
        length(Result, Length),
        Length > 1,
    	AvailablePlaces = OtherAvailablePlaces;
    	AvailablePlaces = [CurrentPlace | OtherAvailablePlaces]
    ).

% Check the intersection for train path in general path and ticket path
check_ticket_intersection(TrainNumber, TicketFrom, TicketTo, Path, Result) :-
    train(TrainNumber, _, Stations, _),
    index_of(Stations, TicketFrom, FromIndex),
    index_of(Stations, TicketTo, ToIndex),
    sublist(TicketPath, FromIndex, ToIndex, Stations),
    intersection(Path, TicketPath, Result).

% Example:
% train_from_to_without_transfers(kharkiv, kyiv, "2019-03-04T17:29Z", X).
% 
% train_from_to_without_transfers(From, To, MinTimeToDeparture, Train -> out)
train_from_to_without_transfers(From, To, MinTimeToDeparture, Train) :- 
    get_stations_by_train(Train, Stations),
    member(StationFrom, Stations),
    member(StationTo, Stations),
    get_station_name(StationFrom, From),
    get_station_name(StationTo, To),
    get_station_departure_time(StationFrom, Departure),
    get_station_arrival_time(StationTo, Arrival),
    parse_time(MinTimeToDeparture, MinTimeToDepartureParsed),
    Departure > MinTimeToDepartureParsed,
    Departure < Arrival.

get_transit(From, To, 0, MinTimeToDeparture, transit(Trains, Path, [])) :-
    train_from_to_without_transfers(From, To, MinTimeToDeparture, Train),
    get_train_number(Train, TrainNumber),
    get_stations_by_train(Train, TrainStations),
    Trains = [TrainNumber],
    index_of(TrainStations, station(From, _, _), FirstIndex),
    index_of(TrainStations, station(To, _, _), LastIndex),
    sublist(Path, FirstIndex, LastIndex + 1, TrainStations).

% get_transit(From -> name, To -> name, NumTransfers, MinTimeToDeparture, Transit -> out).
get_transit(From, To, NumTransfers, MinTimeToDeparture, transit(Trains, Path, Transitions)) :-
    % get CurrentTrain(out), which departs from From(in) and to some Transfer (out) station
    % it should depart later than MinTimeToDeparture
    train_from_to_without_transfers(From, Transfer, MinTimeToDeparture, CurrentTrain),
    
    % Find the Transfer station in CurrentTrain station list and get the arrival time to it
    get_stations_by_train(CurrentTrain, CurrentTrainStations),
    TransferStation = station(Transfer, NewMinTimeToDeparture, _),
    member(TransferStation, CurrentTrainStations),

    % get all trains that pass through Transfer station and depart from it later, 
    % than the previous train arrives at it
    train(_, _, NextTrainStations, _),
    member(station(Transfer, _, Departure), NextTrainStations),
    parse_time(NewMinTimeToDeparture, NewMinTimeToDepartureParsed),
    parse_time(Departure, DepartureTime),
    DepartureTime > NewMinTimeToDepartureParsed,
    
    % Get the arrival time of our next train at the station after the Transition station
    find_element_after(station(Transfer, _, _), NextStation, NextTrainStations),
    get_station_arrival_time_raw(NextStation, NextArrivalTime),
    
    % Get transit for next trains
    NextNumTransfers is NumTransfers - 1,
    get_transit(Transfer, To, NextNumTransfers, NextArrivalTime, transit(NextTrains, NextPath, NextTransitions)),
    
    % Put the train number, its subpath and transfer station in the result
    get_train_number(CurrentTrain, CurrentTrainNumber),
    Trains = [CurrentTrainNumber | NextTrains],
    
    index_of(CurrentTrainStations, station(From, _, _), FirstIndex),
    index_of(CurrentTrainStations, TransferStation, LastIndex),
    sublist(CurrentTrainPath, FirstIndex, LastIndex, CurrentTrainStations),
    append(CurrentTrainPath, NextPath, Path),
    append([Transfer], NextTransitions, Transitions).

% End recursive calls with the last train and available places for it
get_available_places(
    transit([ CurrentTrainNumber ], Path, []),
    PreviousTrainTransition,
    AvailablePlacesFolded
) :-
    member(FirstStation, Path),
    FirstStation = station(PreviousTrainTransition, _, _),
    reverse(Path, ReversedPath),
    nth1(1, ReversedPath, LastStation),
    
    available_places_from_to_by_train(FirstStation, LastStation, CurrentTrainNumber, AvailablePlaces),
    AvailablePlacesFolded = [AvailablePlaces],
    !.

% Get AvailablePlaces using 'transit' object from GetTransit
% as a list of lists of cabs for each train in the list of train numbers
get_available_places(
    transit([CurrentTrainNumber | OtherTrainNumbers], Path, [CurrentTrainTransition | NextTrainTransitions]),
    PreviousTrainTransition,
    AvailablePlaces) :- 
    
    % Get places for other trains
    get_available_places(
        transit(OtherTrainNumbers, Path, NextTrainTransitions), 
        CurrentTrainTransition, 
        OtherAvailablePlaces),
    
    % Find current train's from and to station in subpath and get its cabs without occupied places
    member(FirstStation, Path),
    FirstStation = station(PreviousTrainTransition, _, _),

    member(LastStation, Path),
    LastStation = station(CurrentTrainTransition, _, _),
    
    available_places_from_to_by_train(FirstStation, LastStation, CurrentTrainNumber, AvailableCabs),
    AvailablePlaces = [AvailableCabs | OtherAvailablePlaces],
    !.

% Example:
% transit_and_available_places(lviv, rivne, 1, "2019-03-04T11:30Z", X).
transit_and_available_places(From, To, NumTransfers, MinTime, Result) :-
    get_transit(From, To, NumTransfers, MinTime, Transit),
    Transit = transit(_, Path, _),
	Path = [Head | _],
	Head = station(Name, _, _),
	get_available_places(Transit, Name, AvailablePlaces),
    Result = [Transit | [AvailablePlaces]].

% Example:
% tickets_from_to_by_type(lviv, rivne, 1, "2019-03-04T11:30Z", coupe, X).
tickets_from_to_by_type(From, To, NumTransfers, MinTime, CabType, Result) :-
    transit_and_available_places(From, To, NumTransfers, MinTime, [Transit | [AvailablePlaces]]),
    Transit = transit(Trains, Path, Transfers),
    get_cabs_by_type(AvailablePlaces, CabType, Cabs),
    Path = [Departure | _],
    last(Path, Arrival),
    calculate_price(Cabs, Price),
    findall(Number, member(cab(Number, _, _, _), Cabs), CabNumbers),
    findall(TrainName, 
        (
            member(TrainNumber, Trains),
            train(TrainNumber, TrainName, _, _)
        ),
        TrainNames
    ),
    Result = ticket(Departure, Arrival, Price, TrainNames, Transfers, CabNumbers).

% Sum prices of all Cabs to count TotalPrice for ticket
calculate_price(Cabs, TotalPrice) :- 
    findall(Price, member(cab(_, _, Price, _), Cabs), Prices),
    sum_list(Prices, TotalPrice).

get_cabs_by_type([], _, Cabs) :- Cabs = [].

get_cabs_by_type([CurrentTrainCabs | OtherTrainsCabs], CabType, Cabs) :-
    get_cabs_by_type(OtherTrainsCabs, CabType, OtherCabs),
    get_cab_from_list_by_type(CurrentTrainCabs, CabType, Cab),
    Cabs = [Cab | OtherCabs].

get_cab_from_list_by_type(CabList, CabType, Cab) :-
    member(Cab, CabList),
    Cab = cab(_, CabType, _, _).

sublist(Sublist, FirstIndex, LastIndex, [_Head | Tail]) :-
    FirstIndex > 0, FirstIndex < LastIndex,
    sublist(Sublist, FirstIndex - 1, LastIndex - 1, Tail).
sublist(Sublist, FirstIndex, LastIndex, [Head | Tail]) :-
    0 is FirstIndex, FirstIndex < LastIndex, LastIndex2 is LastIndex - 1,
    Sublist = [Head | Tail2],
    sublist(Tail2, 0, LastIndex2, Tail).
sublist([], 0, 0, _).

% End recursion
index_of([ElementToFind | _], ElementToFind, 0):- !.

% indexOf(List, ElementToFind, Index)
index_of([_|Tail], ElementToFind, Index):-
	index_of(Tail, ElementToFind, Index1),
	!,
	Index is Index1 + 1.

% find_element_after(ElementToFind, ElementOut -> out, List)
find_element_after(ElementToFind, ElementOut, [X0, X1|Xs]) :-
	if_(
        X0 = ElementToFind,
        X1 = ElementOut,
		find_element_after(ElementToFind, ElementOut, [X1|Xs])
	).

if_(Goal_, Then_, Else_) :-
	call(Goal_, Result),
	(
		Result == true -> call(Then_);
   		Result == false -> call(Else_);
    	nonvar(Result) -> throw(error(type_error(boolean, Result), _));
    	/* var(Result) */ throw(error(instantiation_error, _))
   ).

=(X, Y, T) :-
	(
    X == Y -> T = true;
    X \= Y -> T = false;
    T = true, X = Y;
    T = false,
    dif(X, Y)
).

