lsst-ctrl-bps-panda v30.0.1 (2026-02-03)
========================================

Dropped support for Python 3.11.
Now tested with Python 3.14.

Other Changes and Additions
---------------------------

- - Removed unused ``isort`` and ``black`` sections from ``pyproject.toml``.
  - Bumped minimum Python version to 3.12.
  - Switched docs action to use ``sphinxutils``. (`DM-54031 <https://rubinobs.atlassian.net/browse/DM-54031>`_)


lsst-ctrl-bps-panda v30.0.0 (2026-01-16)
========================================

New Features
------------

- Added refresh function in panda_auth (`DM-48912 <https://rubinobs.atlassian.net/browse/DM-48912>`_)
- Now use job name to map the quantum nodes (`DM-50973 <https://rubinobs.atlassian.net/browse/DM-50973>`_)
- Support different maxPayloadsPerPandaJob for different ES tasks (`DM-52454 <https://rubinobs.atlassian.net/browse/DM-52454>`_)
- Added parts to set task dependency (`DM-52585 <https://rubinobs.atlassian.net/browse/DM-52585>`_)
- Updated ``bps report`` function to aggregate panda task slices into task labels (`DM-52866 <https://rubinobs.atlassian.net/browse/DM-52866>`_)
- Now split huge a workflow into smaller steps (`DM-52999 <https://rubinobs.atlassian.net/browse/DM-52999>`_)


Bug Fixes
---------

- Fixed the ``order_id`` for ``EventService`` (``EventService`` requires the ``order_id`` to be continuous. When a big task is split to multiple tasks, the ``order_id`` was not continuous) (`DM-52283 <https://rubinobs.atlassian.net/browse/DM-52283>`_)


lsst-ctrl-bps-panda v29.1.0 (2025-06-13)
========================================

New Features
------------

- Enabled environment variables to be set in BPS YAML files (`DM-49801 <https://rubinobs.atlassian.net/browse/DM-49801>`_)
- Added get_status method to ``PanDAService`` class for quick checking of run status. (`DM-50619 <https://rubinobs.atlassian.net/browse/DM-50619>`_)
- Now use a map file to reduce the size of the BPS PanDA submission size (`DM-50973 <https://rubinobs.atlassian.net/browse/DM-50973>`_)


Bug Fixes
---------

- Fixed ``fileDistributionEndPoint`` for different protocols (`DM-49020 <https://rubinobs.atlassian.net/browse/DM-49020>`_)
- Passed ``IDDS_MAX_NAME_LENGTH`` to remote build task (`DM-50400 <https://rubinobs.atlassian.net/browse/DM-50400>`_)


Other Changes and Additions
---------------------------

- Updated test to pass label to GenericWorkflowJob's constructor. (`DM-46294 <https://rubinobs.atlassian.net/browse/DM-46294>`_)


lsst-ctrl-bps-panda v29.0.0 (2025-03-25)
========================================

New Features
------------

- Modified to allow execution of jobs remotely without the necessity to use the remote build approach. (`DM-46307 <https://rubinobs.atlassian.net/browse/DM-46307>`_)


Bug Fixes
---------

- Fixed the passing of processing_type to different jobs (`DM-47906 <https://rubinobs.atlassian.net/browse/DM-47906>`_)


Other Changes and Additions
---------------------------

- Migrated configuration files to use the pipelines built for AlmaLinux (`DM-48967 <https://rubinobs.atlassian.net/browse/DM-48967>`_)


lsst-ctrl-bps-panda v28.0.0 (2024-11-21)
========================================

New Features
------------

- Updated to support event service which allows multiple short payload jobs to run in a single PanDA job for efficiency. (`DM-38177 <https://rubinobs.atlassian.net/browse/DM-38177>`_)


Other Changes and Additions
---------------------------

- Removed ``requestMemory``, ``memoryMultipler`` and ``numberOfRetries`` from since those are now defined in ``ctrl_bps`` (`DM-44513 <https://rubinobs.atlassian.net/browse/DM-44513>`_)
- Fixed ``pandaDistributionEndpoint`` to support different protocols (`DM-45631 <https://rubinobs.atlassian.net/browse/DM-45631>`_)
- Removed support for execution butler for remote job submission (`DM-46845 <https://rubinobs.atlassian.net/browse/DM-46845>`_)


lsst-ctrl-bps-panda v27.0.0 (2024-06-04)
========================================

New Features
------------

- Mapped bps memory boosting attributes to PanDA memory boosting attributes (`DM-36981 <https://rubinobs.atlassian.net/browse/DM-36981>`_)
- Updated the open-source license to allow for the code to be distributed with either GPLv3 or BSD 3-clause license. (`DM-37231 <https://rubinobs.atlassian.net/browse/DM-37231>`_)
- Updated ``panda-service.py`` to return exit code information. (`DM-41543 <https://rubinobs.atlassian.net/browse/DM-41543>`_)


Bug Fixes
---------

- Restored error message about too long pseudo filename while preparing workflow. (`DM-40699 <https://rubinobs.atlassian.net/browse/DM-40699>`_)
- Fixed a typo in the reference of a job attribute. (`DM-42090 <https://rubinobs.atlassian.net/browse/DM-42090>`_)
- Fixed report function during checking of request status. (`DM-42528 <https://rubinobs.atlassian.net/browse/DM-42528>`_)
- * Fixed bps panda report function when no tasks are created (when no tasks are created, a SQL outer join will create an empty row which seems like a task is created).
  * Fixed bps panda report function when a build task fails and doesn't report any file information. (`DM-42788 <https://rubinobs.atlassian.net/browse/DM-42788>`_)


Other Changes and Additions
---------------------------

- Removed error message about too long pseudo filename while preparing workflow as the length is now checked by iDDS. (`DM-41545 <https://rubinobs.atlassian.net/browse/DM-41545>`_)


lsst-ctrl-bps-panda v26.0.0 (2023-09-25)
========================================

New Features
------------

- Enabled saving of iDDS client workflow objects at prepare bps submission stage. (`DM-34915 <https://rubinobs.atlassian.net/browse/DM-34915>`_)
- Updated BPS PanDA plugin to work with quantum-backed butler. (`DM-39553 <https://rubinobs.atlassian.net/browse/DM-39553>`_)


Bug Fixes
---------

- Fixed the execution butler transfer bug when period in run collection. (`DM-37843 <https://rubinobs.atlassian.net/browse/DM-37843>`_)
- Fixed PanDA task chunking bug that caused assertion error during submission for really large QuantumGraphs. (`DM-38101 <https://rubinobs.atlassian.net/browse/DM-38101>`_)
- Handled dependency issues when preparing rescue workflows. (`DM-38377 <https://rubinobs.atlassian.net/browse/DM-38377>`_)


Other Changes and Additions
---------------------------

- Now print out pseudo_file_name in the bps PanDA plugin to simplify debugging if there is a problem with it being too long. (`DM-37352 <https://rubinobs.atlassian.net/browse/DM-37352>`_)
- Included butler repo URL in log message labels. (`DM-37961 <https://rubinobs.atlassian.net/browse/DM-37961>`_)
- Modified PanDA task chunking to be evenly divided. (`DM-38101 <https://rubinobs.atlassian.net/browse/DM-38101>`_)
- Updated ``ctrl_bps_panda/config/bps_usdf.yaml`` to allow for local custom setup (`DM-38142 <https://rubinobs.atlassian.net/browse/DM-38142>`_)
- Updated some default YAML values to more easily allow parts to be
  modified as well as provided values to go with the updated bps
  default YAML (e.g., no longer need ``runQuantumCommands``). (`DM-38307 <https://rubinobs.atlassian.net/browse/DM-38307>`_)
- Moved ``fileDistributionEndPoint`` from lustre to weka in USDF configuration. (`DM-39334 <https://rubinobs.atlassian.net/browse/DM-39334>`_)


lsst-ctrl-bps-panda v25.0.0 (2023-03-02)
========================================

New Features
------------

- Added cancel, restart, report and ping functions in bps panda plugin. (`DM-34964 <https://rubinobs.atlassian.net/browse/DM-34964>`_)
- Added ``setupLSSTEnv`` in ``bps_usdf.yaml`` which can be updated to setup developer lsst pipelines stack. (`DM-36376 <https://rubinobs.atlassian.net/browse/DM-36376>`_)


Bug Fixes
---------

- Fixed the bug that bps-panda reports success when there is an authentication permission error. (`DM-35364 <https://rubinobs.atlassian.net/browse/DM-35364>`_)
- Fixed the setting of ``number_of_retries`` to `None` in ``idds_tasks``. (`DM-35508 <https://rubinobs.atlassian.net/browse/DM-35508>`_)
- Fixed the bug that iDDS results can be something other than a string. (`DM-35964 <https://rubinobs.atlassian.net/browse/DM-35964>`_)


Other Changes and Additions
---------------------------

- Added the ability to prioritize dev/test tasks
  * ``prodSourceLabel``: it can be configured in the submission yaml, by default it is 'managed'
  * ``priority``: it can be set in the submission yaml, by default it is 500 (`DM-36375 <https://rubinobs.atlassian.net/browse/DM-36375>`_)


lsst-ctrl-bps-panda v24.0.0 (2022-08-29)
========================================

New Features
------------

- This package has been extracted from ``lsst_ctrl_bps`` into a standalone package to make it easier to manage development of the PanDA plugin.
  (`DM-33521 <https://rubinobs.atlassian.net/browse/DM-33521>`_)
- Introduced a new parameter ``dockerImageLocation`` in the PanDA IDF configuration yaml file to pull lsst release containers from **GAR (Google Artifact Registry)**. This parameter is trailed with ``'/'``, so it could be used in ``sw_image`` path in the following example. And the ``sw_image`` will still refer to the **Docker hub**, if the parameter ``dockerImageLocation`` is empty or not defined, to make the ``sw_image`` backward compatible with previous PanDA IDF configuration yaml files.

  In the user bps submission yaml file, just prepend this parameter to the sw_image path, that is:

  .. code-block:: YAML

     sw_image: "{dockerImageLocation}lsstsqre/centos:7-stack-lsst_distrib-w_2022_05"

  Please note that there is no extra character(s) between ``{dockerImageLocation}`` and ``lsstsqre``.

  In case you have to use images from the Docker hub instead, you just take out the prefix ``{dockerImageLocation}`` in the path, that is:

  .. code-block:: YAML

     sw_image: "lsstsqre/centos:7-stack-lsst_distrib-w_2022_05" (`DM-32992 <https://rubinobs.atlassian.net/browse/DM-32992>`_)

Bug Fixes
---------

- Update the path to the command line decoder in the config file and the documentation. (`DM-34574 <https://rubinobs.atlassian.net/browse/DM-34574>`_)


Other Changes and Additions
---------------------------

- Changed the parameter ``runnerCommand`` in the PanDA IDF example yaml file, to start ``prmon`` to monitor the memory usage of the payload job.
  This executable ``prmon`` is only available in releases after ``w_2022_05``. (`DM-32579 <https://rubinobs.atlassian.net/browse/DM-32579>`_)
- Make the PanDA example config more easily runnable from data-int RSP (`DM-32695 <https://rubinobs.atlassian.net/browse/DM-32695>`_)

- * PanDA cloud was mapped from BPS compute site, fixed it.
  * Pass BPS cloud to PanDA cloud.
  * Add supports for task priority, vo, working group, prodSourceLabel. (`DM-33889 <https://rubinobs.atlassian.net/browse/DM-33889>`_)
- Remove ``iddsServer`` from ``bps_idf.yml``, to use the iDDS server defined in the PanDA relay service.
   Remove ``IDDS_CONFIG`` requirements (requiring ``idds`` version 0.10.6 and later). (`DM-34106 <https://rubinobs.atlassian.net/browse/DM-34106>`_)
- Add missing ``__all__`` statement to make the documentation render properly at https://pipelines.lsst.io. (`DM-34921 <https://rubinobs.atlassian.net/browse/DM-34921>`_)

ctrl_bps v23.0.1 (2022-02-02)
=============================

New Features
------------

- * Large tasks (> 30k jobs) splitted into chunks
  * Updated iDDS API usage for the most recent version
  * Updated iDDS API initialization to force PanDA proxy using the IAM user name for submitted workflow
  * Added limit on number of characters in the task pseudo inputs (`DM-32675 <https://rubinobs.atlassian.net/browse/DM-32675>`_)
- * New ``panda_auth`` command for handling PanDA authentication token.
    Includes status, reset, and clean capabilities.
  * Added early check of PanDA authentication token in submission process. (`DM-32830 <https://rubinobs.atlassian.net/browse/DM-32830>`_)

Other Changes and Additions
---------------------------

- * Changed printing of submit directory early.
  * Changed PanDA plugin to only print the numeric id when outputing the request/run id.
  * Set maximum number of jobs in a PanDA task (maxJobsPerTask) to 70000 in config/bps_idf.yaml. (`DM-32830 <https://rubinobs.atlassian.net/browse/DM-32830>`_)

ctrl_bps v23.0.0 (2021-12-10)
=============================

Other Changes and Additions
---------------------------

- Provide a cleaned up version of default config yaml for PanDA-plugin on IDF (`DM-31476 <https://rubinobs.atlassian.net/browse/DM-31476>`_)
