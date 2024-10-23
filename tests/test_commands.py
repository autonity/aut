# import autonity_cli
# from autonity_cli import main
# from autonity_cli.commands import get
# from unittest import TestCase

# class TestAutNoRPCModule(TestCase):
#     def test_list(self):
#         with self.assertRaises(SystemExit) as cm:
#             aut.main.aut(['list','--foobar'])
#         self.assertEqual(cm.exception.code, 64)
#     def test_get(self):
#         with self.assertRaises(SystemExit) as cm:
#             aut.main.aut(['get','--foobar'])
#         self.assertEqual(cm.exception.code, 64)
#     def test_maketx(self):
#         with self.assertRaises(SystemExit) as cm:
#             aut.main.aut(['maketx','--foobar'])
#         self.assertEqual(cm.exception.code, 64)
#         with self.assertRaises(SystemExit) as cm:
#             aut.main.aut(
#               ['maketx','-f','0xfoobar','-t','0x6C874d2c048A9D6943BAe1b1c364BF4AF9454c42',
#                '-g','21000','-P',"2gwei"])
#         self.assertEqual(cm.exception.code, 65)
#     def test_signtx(self):
#         with self.assertRaises(SystemExit) as cm:
#             aut.main.aut(['signtx','--foobar'])
#         self.assertEqual(cm.exception.code, 64)
#     def test_sendtx(self):
#         with self.assertRaises(SystemExit) as cm:
#             aut.main.aut(['sendtx','--foobar'])
#         self.assertEqual(cm.exception.code, 64)
