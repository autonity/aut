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
}
