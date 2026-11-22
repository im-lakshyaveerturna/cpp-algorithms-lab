CXX = c++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra -Wpedantic -Werror
PYTHON ?= python3
SANITIZER_FLAGS = -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -O1 -g
SANITIZER_TIMEOUT_SECONDS ?= 120

.PHONY: all test sanitize graphs clean
all:
	$(MAKE) -C sorting all CXX="$(CXX)" CXXFLAGS="$(CXXFLAGS)"
	mkdir -p daa/build
	@for source in daa/programs/*.cpp; do \
		program=daa/build/$$(basename "$$source" .cpp); \
		$(CXX) $(CXXFLAGS) "$$source" -o "$$program" || exit; \
	done

test:
	$(MAKE) -C sorting test CXX="$(CXX)" CXXFLAGS="$(CXXFLAGS)" PYTHON="$(PYTHON)"
	CXX="$(CXX)" CXXFLAGS="$(CXXFLAGS)" $(PYTHON) daa/tests/test_algorithms.py

sanitize:
	$(MAKE) -C sorting sanitize CXX="$(CXX)" PYTHON="$(PYTHON)"
	DAA_PROGRAM_TIMEOUT_SECONDS="$(SANITIZER_TIMEOUT_SECONDS)" CXX="$(CXX)" CXXFLAGS="$(SANITIZER_FLAGS)" $(PYTHON) daa/tests/test_algorithms.py

graphs:
	$(PYTHON) sorting/scripts/plot_comparisons.py
	$(PYTHON) sorting/scripts/summarize_results.py

clean:
	$(MAKE) -C sorting clean
	rm -rf daa/build
