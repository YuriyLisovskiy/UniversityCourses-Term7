#ifndef RLE_TIME_TRACKER_H
#define RLE_TIME_TRACKER_H

#include <map>
#include <string>
#include <chrono>


struct TimingData
{
	double reading_time = 0.0;
	double writing_time = 0.0;
	double encoding_time = 0.0;
	double decoding_time = 0.0;
};


class TimeTracker
{
private:
	class Timer
	{
	public:
		Timer();
		void reset();
		[[nodiscard]] double elapsed() const;

	private:
		typedef std::chrono::high_resolution_clock clock_;
		typedef std::chrono::duration<double, std::milli> second_;

		std::chrono::time_point<clock_> _begin;
	};

	std::map<std::string, Timer> _timers;

	bool exists(const std::string& key);

public:
	void start(const std::string& tracker);
	void reset(const std::string& tracker);
	double elapsed(const std::string& tracker);
};


#endif // RLE_TIME_TRACKER_H
