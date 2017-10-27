This file, when parsed should return an array of two components:
TestComponent1/20k/Meow Qty: 1
TestComponent2/25K/Meow Qty: 2

$Comp
L TestComponent1 Ref1
F 0 "NONSENSE"
F 1 "20K"
F 2 "Meow"
$EndComp

Should not be parsed

$Comp
L TestComponent2 Ref2
F 0 "NONSENSE"
F 1 "25K"
F 2 "Meow"
$EndComp

Should Not be parsed

$Comp
L TestComponent2 Ref3
F 0 "NONSENSE"
F 1 "25K"
F 2 "Meow"
$EndComp