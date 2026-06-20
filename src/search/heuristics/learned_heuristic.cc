#include "learned_heuristic.h"

#include "../plugins/plugin.h"
#include "../task_utils/task_properties.h"
#include "../utils/logging.h"

#include "../ext/httplib.h"
#include "../ext/json.hpp"

#include <cstddef>
#include <limits>
#include <utility>

#include <cassert>


using namespace std;
using json = nlohmann::json;

namespace learned_heuristic {
// construction and destruction
LearnedHeuristic::LearnedHeuristic(
    const shared_ptr<AbstractTask> &transform, bool cache_estimates,
    const string &description, utils::Verbosity verbosity)
    : Heuristic(transform, cache_estimates, description, verbosity){
    if (log.is_at_least_normal()) {
        log << "Initializing learned heuristic..." << endl;
    }
}



int LearnedHeuristic::compute_heuristic(const State &state) { // TODO: What is this ancestor state nonsense?
    // 1. Convert state to JSON/string
    // 2. POST to web service
    // 3. Read integer response
    // 4. Return heuristic value

    // 1. Convert state to JSON/string
    json request_json;
    
    state.unpack();
    request_json["state"] = state.get_unpacked_values();  // TODO: What state representation does Ferber train on?

    // 2. POST to web service
    httplib::Client cli("localhost", 8080);
    if (log.is_at_least_normal()) {
        log << "Calling learned heuristic..." << endl;
    }
    // Connectivity test
    //auto response = cli.Get("/");
    auto response = cli.Post(
        "/heuristic",
        request_json.dump(),
        "application/json"
    );

    if (response && response->status == 200) {
        if (log.is_at_least_normal()) {
            log << "Response status: 200..." << endl;
        }

        json response_json = json::parse(response->body);

        int heuristic_value = response_json["heuristic"].get<int>();
        if (log.is_at_least_normal()) {
            log << "Heuristic value: " << heuristic_value << endl;
        }

        return heuristic_value;  
    }


    //auto response = cli.Post(
    //     "/heuristic",
    //     request_json.dump(),
    //     "application/json"
    // );
    
    return 0;
}


class LearnedHeuristicFeature
    : public plugins::TypedFeature<Evaluator, LearnedHeuristic> {
public:
    LearnedHeuristicFeature() : TypedFeature("learned") {
        document_title("Learned heuristic");
        document_synopsis(
            "A placeholder for a learned heuristic. Just a stub for now. Always reutrns 0 at the moment.");

        add_heuristic_options_to_feature(*this, "learned");

        //document_language_support("action costs", "supported");
        //document_language_support("conditional effects", "supported");
        //document_language_support("axioms", "supported");

        //document_property("admissible", "yes");
        //document_property("consistent", "yes");
        //document_property("safe", "yes");
        //document_property("preferred operators", "no");
    }

    virtual shared_ptr<LearnedHeuristic> create_component(  // TODO: What is this for?
        const plugins::Options &opts) const override {
        return plugins::make_shared_from_arg_tuples<LearnedHeuristic>(
            get_heuristic_arguments_from_options(opts));
    }
};

static plugins::FeaturePlugin<LearnedHeuristicFeature> _plugin; 
}
