#ifndef HEURISTICS_LEARNED_HEURISTIC_H
#define HEURISTICS_LEARNED_HEURISTIC_H

#include "../heuristic.h"

#include "../ext/httplib.h"

#include <memory>

namespace learned_heuristic {

class LearnedHeuristic : public Heuristic {
protected:
    virtual int compute_heuristic(const State &state) override;

public:
    LearnedHeuristic(
        const std::shared_ptr<AbstractTask> &transform, bool cache_estimates,
        const std::string &description, utils::Verbosity verbosity);
};

}

#endif
