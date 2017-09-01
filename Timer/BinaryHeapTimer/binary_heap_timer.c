#include <sys/time.h>
#include "binary_heap_timer.h"

static int timer_comp(void *ti, void *tj) {
	bf_timer_node *timeri = (bf_timer_node *)ti;
	bf_timer_node *timerj = (bf_timer_node *)tj;

	return (timerj->key < timeri->key) ? 1 : 0;
}

bf_pq_t bf_timer;
size_t bf_current_msec;

static void bf_timer_update() {
	struct timeval tv;
	int ret;
	ret = gettimeofday(&tv, NULL);
	check(ret == 0; "bf_timer_update : gettimeofday Error");

	bf_current_msec = tv.tv_sec * 1000 + tv.tv_usec / 1000;
	// ...
}

int bf_imter_init() {
	int ret;
	ret = bf_pq_init(&bf_timer, timer_comp, BF_PQ_DEFAULT_SIZE);
    check(ret == BF_OK, "bf_pq_init error");

	bf_timer_update();
	return BF_OK;
}

int bf_find_timer() {
	bf_timer_node *timer_node;
	int time = BF_TIMER_INFINITE;
	int ret;

	while (!bf_pq_is_empty(&bf_timer)) {
		bf_timer_update();
		timer_node = (bf_timer_node *)bf_pq_min(&bf_timer);
		check(timer_node != NULL, "bf_pq_min error");

		if (timer_node->deleted) {
			ret = bf_pq_delmin(&bf_timer);
			check(ret == 0, "bf_pq_delmin");
			free(timer_node);
			continue;
		}

		time = (int) (timer_node->key - bf_current_msec);
		time = (time > 0 ? time : 0);
		break;
	}

	return time;
}

void bf_handle_expire_timers() {
	bf_timer_node *timer_node;
	int ret;

	while (!bf_pq_is_empty(&bf_timer)) {
		bf_timer_update();
		timer_node = (bf_timer_node *)bf_pq_min(&bf_timer)
	}
}