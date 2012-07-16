/*
    Copyright (C) 2012 Samsung Electronics
    Copyright (C) 2012 Intel Corporation. All rights reserved.

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this library; if not, write to the Free Software Foundation,
    Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
*/

#include "config.h"
#include "EWK2UnitTestEnvironment.h"

namespace EWK2UnitTest {

EWK2UnitTestEnvironment::EWK2UnitTestEnvironment(bool useX11Window)
    : m_defaultWidth(800)
    , m_defaultHeight(600)
    , m_useX11Window(useX11Window)
{
}

const char* EWK2UnitTestEnvironment::defaultTestPageUrl() const
{
    return "file://"TEST_RESOURCES_DIR"/default_test_page.html";
}

} // namespace EWK2UnitTest
