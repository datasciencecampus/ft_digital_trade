##  Code review

All code needs to follow the planets CONTRIBUTING guidelines as set out in *CONTRIBUTING.md*

- [] **CONTRIBUTING guidelines**: Guidelines are followed and deviations are rare, necessary and explained.

#### Documentation

Any new code includes all the following forms of documentation:

- [] **Function Documentation**
- [] **Script Documentation** Scripts are documented in line with the CONTRIBUTING guidelines

#### Functionality

- [] **Document and build**: Check the file or notebook runs sequentially
- [] **Packages** Check the required packages
- [] **Automated tests**: Unit tests cover essential functions for a reasonable range
  of inputs and conditions. All tests pass on your local machine. Ideally for all functions

### AQA

- [] ** Check ** give a brief overview of the QA process that has been followed
- [] ** document ** document QA checks where relevant
- [ ] developments adhere to AQA plan (see `docs/aqa/aqa_plan.md`). QA plan updated if necessary
- [ ] data log updated (see `docs/aqa/data_log.md`), if necessary
- [ ] assumptions, and caveats log updated (see `docs/aqa/assumptions_caveats.md`), if
  necessary

#### Final approval (post-review)

The author has responded to my review and made changes to my satisfaction.
- [] **I recommend merging this request.**

---

### Review comments

*Insert detailed comments here!*

These might include, but not exclusively:

- bugs that need fixing (does it work as expected? and does it work with other code
  that it is likely to interact with?)
- alternative methods (could it be written more efficiently or with more clarity?)
- documentation improvements (does the documentation reflect how the code actually works?)
- additional tests that should be implemented (do the tests effectively assure that it
  works correctly?)
- code style improvements (could the code be written more clearly?)
- QA checks that have failed or outputs that look suspicious
- Is QA sufficient for the purpose of the code?

Your suggestions should be tailored to the code that you are reviewing.
Be critical and clear, but not mean. Ask questions and set actions.
