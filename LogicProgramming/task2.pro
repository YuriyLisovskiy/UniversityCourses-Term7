use_module(library(date)).

% station(StationName, DepartureTime, ArrivalTime)
% station(st1, "2017-08-11T12:30Z", "2017-08-11T12:30Z").
% station(st2, "2017-08-11T13:40Z", "2017-08-11T13:50Z").
% station(st3, "2017-08-11T14:30Z", "2017-08-11T14:40Z").
% station(st4, "2017-08-11T16:40Z", "2017-08-11T16:40Z").
% station(st5, "2017-08-11T06:00", "2017-08-11T06:00Z").
% station(st6, "2017-08-11T08:40Z", "2017-08-11T08:50Z").
% station(st7, "2017-08-11T11:30Z", "2017-08-11T11:40Z").
% station(st8, "2017-08-11T16:40Z", "2017-08-11T16:40Z").

% train(Number, Name, ListOfStations)
train(
    1,
    "st1-st3",
    [
    	station(st1, "2017-08-11T12:30Z", "2017-08-11T12:30Z"),
		station(st2, "2017-08-11T13:40Z", "2017-08-11T13:50Z"),
		station(st3, "2017-08-11T14:30Z", "2017-08-11T14:40Z")
    ]
).
train(
    2,
    "st3-st4",
    [
    	station(st3, "2017-08-11T14:30Z", "2017-08-11T14:40Z"),
		station(st4, "2017-08-11T16:40Z", "2017-08-11T16:40Z")
    ]
).
train(
    3,
    "st3-st7",
    [
    	station(st3, "2017-08-11T14:30Z", "2017-08-11T14:40Z"),
		station(st4, "2017-08-11T16:40Z", "2017-08-11T16:40Z"),
		station(st5, "2017-08-11T06:00", "2017-08-11T06:00Z"),
		station(st6, "2017-08-11T08:40Z", "2017-08-11T08:50Z"),
		station(st7, "2017-08-11T11:30Z", "2017-08-11T11:40Z"),
    ]
).
train(
    4,
    "st3-st8",
    [
    	station(st3, "2017-08-11T14:30Z", "2017-08-11T14:40Z"),
		station(st4, "2017-08-11T16:40Z", "2017-08-11T16:40Z"),
		station(st8, "2017-08-11T16:40Z", "2017-08-11T16:40Z")
    ]
).
train(
    5,
    "st5-st1",
    [
    	station(st5, "2017-08-11T06:00", "2017-08-11T06:00Z"),
    	station(st1, "2017-08-11T12:30Z", "2017-08-11T12:30Z"),
		station(st2, "2017-08-11T13:40Z", "2017-08-11T13:50Z")
    ]
).
train(
    6,
    "st6-st3",
    [
    	station(st6, "2017-08-11T08:40Z", "2017-08-11T08:50Z"),
      	station(st5, "2017-08-11T06:00", "2017-08-11T06:00Z"),
      	station(st8, "2017-08-11T16:40Z", "2017-08-11T16:40Z"),
      	station(st1, "2017-08-11T12:30Z", "2017-08-11T12:30Z"),
		station(st2, "2017-08-11T13:40Z", "2017-08-11T13:50Z"),
		station(st3, "2017-08-11T14:30Z", "2017-08-11T14:40Z")
    ]
).
train(
    7,
    "st8-st2",
    [
    	station(st8, "2017-08-11T16:40Z", "2017-08-11T16:40Z"),
      	station(st1, "2017-08-11T12:30Z", "2017-08-11T12:30Z"),
		station(st2, "2017-08-11T13:40Z", "2017-08-11T13:50Z")
    ]
).
train(
    8,
    "st-st",
    [
    	
    ]
).
train(
    9,
    "st-st",
    [
    	
    ]
).
train(
    10,
    "st-st",
    [
    	
    ]
).

train_from_to(From, To, Name) :- 
    train(_, Name, From, To, _, _).

