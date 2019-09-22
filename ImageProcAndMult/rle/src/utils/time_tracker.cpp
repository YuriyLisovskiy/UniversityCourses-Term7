#include "time_tracker.h"


TimeTracker::Timer::Timer() : _begin(clock_::now())
{
}

void TimeTracker::Timer::reset()
{
	this->_begin = clock_::now();
}

double TimeTracker::Timer::elapsed() const
{
	return std::chrono::duration_cast<second_>(clock_::now() - this->_begin).count();
}

bool TimeTracker::exists(const std::string& key)
{
	return this->_timers.find(key) != this->_timers.end();
}

void TimeTracker::start(const std::string& tracker)
{
	if (this->exists(tracker))
	{
		throw std::invalid_argument("tracker already exists");
	}

	this->_timers[tracker] = TimeTracker::Timer();
}

void TimeTracker::reset(const std::string& tracker)
{
	if (!this->exists(tracker))
	{
		throw std::invalid_argument("tracker does not exist");
	}

	this->_timers[tracker].reset();
}

double TimeTracker::elapsed(const std::string& tracker)
{
	if (!this->exists(tracker))
	{
		throw std::invalid_argument("tracker does not exist");
	}

	return this->_timers[tracker].elapsed();
}
