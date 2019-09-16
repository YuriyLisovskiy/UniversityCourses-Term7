#ifndef RLE_TIME_TRACKER_H
#define RLE_TIME_TRACKER_H

#include <map>
#include <string>


class TimeTracker
{
private:
	class Item
	{
		
	};

public:
	void start(const std::string& tracker);
	void stop(const std::string& tracker);
	double track(const std::string& tracker);
};


#endif // RLE_TIME_TRACKER_H
