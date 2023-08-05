-- This is a dummy LUA which sole purpose is to test 
-- the freshly generated Harfang LUA package.
hg = require "harfang"

for k,v in pairs(hg) do
    print(k)
end
