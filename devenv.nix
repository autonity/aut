{ pkgs, ... }:

{
  packages = [
    pkgs.hatch
  ];

  languages.python = {
    enable = true;
    version = "3.12";
    venv.enable = false;
  };

  enterShell = ''
    test -d ./autonity.py && ENV=local || ENV=default
    hatch run $ENV:true  # Create virtualenv at first run
    export VIRTUAL_ENV="$(hatch env find $ENV)"
    export HATCH_ENV_ACTIVE=$ENV
    export PATH="$VIRTUAL_ENV/bin:$PATH"
  '';
}
