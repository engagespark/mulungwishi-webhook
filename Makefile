.PHONY: clean clean_remote pull_remote installdeps_remote deploy

USER=mulungwishi
HOST=104.251.216.252
SSH_KEY=~/.ssh/mulungwishi_rsa
CONNECT_TO_REMOTE=ssh -i $(SSH_KEY) -t $(USER)@$(HOST)

# colors
INFO:=$(shell echo "\033[0;36m")
SUCCESS:=$(shell echo "\033[0;32m")
END:=$(shell echo "\033[0m")


# commands
CLEAN=find . | grep -E '(__pycache__|\.pyc|\.pyo$$)' | xargs rm -rfv
CD=cd /opt/webapps/mulungwishi
PULL=git pull
ACTIVATE=source /opt/pyenv/versions/3.5.1/envs/mulungwishi/bin/activate
INSTALL=pip install -r requirements.txt
TAIL_ACCESS=sudo tail -f /var/log/gunicorn/mulungwishi-access.log
TAIL_ERROR=sudo tail -f /var/log/gunicorn/mulungwishi-error.log
RESTART_APP=sudo service mulungwishi restart


# local tasks
clean:
	@echo "$(INFO)Removing python bytecode files on local...$(END)"
	@$(CLEAN)
	@echo "$(INFO)Finished removing python bytecode files on local.$(END)"
	@echo

# remote tasks
clean_remote:
	@echo "$(INFO)Removing python bytecode files on remote...$(END)"
	@$(CONNECT_TO_REMOTE) "$(CLEAN)"
	@echo "$(INFO)Finished removing python bytecode files on remote.$(END)"
	@echo

pull_remote: clean
	@echo "$(INFO)Synchronizing server code with git repository...$(END)"
	@$(CONNECT_TO_REMOTE) "$(CD) && $(PULL)"
	@echo "$(INFO)Finished synchronizing server code with git repository.$(END)"
	@echo

installdeps_remote:
	@echo "$(INFO)Installing/updating project dependencies on remote...$(END)"
	@$(CONNECT_TO_REMOTE) "$(ACTIVATE) && $(CD) && $(INSTALL)"
	@echo "$(INFO)Finished installing/updating project dependencies on remote.$(END)"
	@echo

tail_access:
	@echo "$(INFO)Tailing access log on remote...$(END)"
	@$(CONNECT_TO_REMOTE) "$(TAIL_ACCESS)"
	@echo "$(INFO)Finished access log on remote.$(END)"
	@echo

tail_error:
	@echo "$(INFO)Tailing error log on remote...$(END)"
	@$(CONNECT_TO_REMOTE) "$(TAIL_ERROR)"
	@echo "$(INFO)Finished error log on remote.$(END)"
	@echo

deploy: clean_remote pull_remote installdeps_remote
	@echo "$(INFO)Restarting application...$(END)"
	@$(CONNECT_TO_REMOTE) "$(RESTART_APP)"
	@echo "$(INFO)Finished restarting application.$(END)"
	@echo
	@echo "$(SUCCESS)Deployment successful.$(END)"
	@echo
